import sys
import importDXF, os, tempfile, subprocess, sys, shutil , dotenv
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# sys.path.append(os.environ.get('FREECAD_LIB'))
# sys.path.append(os.environ.get('FREECAD_BIN'))
# sys.path.append(r'D:\Dev Tools\FreeCAD\FreeCAD_0.19.22670-Win-Conda_vc14.x-x86_64\bin\Lib\site-packages')
import six
import FreeCAD as app
import FreeCADGui as gui
from FreeCAD import Console as FCC


from datetime import datetime


if FreeCAD.GuiUp:
    from DraftTools import translate
else:
    def translate(context, txt):
        return txt

# Save the native open function to avoid collisions
if open.__module__ == '__builtin__':
    pythonopen = open


def open(filename):
    """Open filename and parse using importDXF.open().
    Parameters
    ----------
    filename : str
        The path to the filename to be opened.
    Returns
    -------
    App::Document
        The new FreeCAD document object created, with the parsed information.
    """
    dxf = convertToDxf(filename)
    if dxf:
        doc = importDXF.open(dxf)
        return doc
    return


def insert(filename, docname):
    """Imports a file using importDXF.insert().
    If no document exist, it is created.
    Parameters
    ----------
    filename : str
        The path to the filename to be opened.
    docname : str
        The name of the active App::Document if one exists, or
        of the new one created.
    Returns
    -------
    App::Document
        The active FreeCAD document, or the document created if none exists,
        with the parsed information.
    """
    dxf = convertToDxf(filename)
    if dxf:
        # Warning: function doesn't return?
        doc = importDXF.insert(dxf, docname)
        return doc
    return


def export(objectslist, filename):
    """Export the DWG file with a given list of objects.
    The objects are exported with importDXF.export().
    Then the result is converted to DWG.
    Parameters
    ----------
    exportList : list
        List of document objects to export.
    filename : str
        Path to the new file.
    Returns
    -------
    str
        The same `filename` input.
    """
    
    _basename = os.path.splitext(os.path.basename(filename))[0]
    dxf = tmp_folder + os.sep + _basename + ".dxf"
    importDXF.export(objectslist, dxf)
    convertToDwg(dxf, filename)
    return filename


def getTeighaConverter():
    """Find the ODA (formerly Teigha) executable.
    It searches the FreeCAD parameters database, then searches for common
    paths in Linux and Windows systems.
    Parameters
    ----------
    None
    Returns
    -------
    str
        The full path of the converter executable
        '/usr/bin/TeighaFileConverter'
    """
    return oda_path #r"D:\Program Files\ODA\ODAFileConverter_title 21.9.0\ODAFileConverter.exe"
    import FreeCAD, os, platform
    p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft")
    p = p.GetString("TeighaFileConverter")
    if p:
        # path set manually
        teigha = p
    else:
        # try to find teigha
        teigha = None
        print("none")
        if platform.system() == "Linux":
            teigha = "/usr/bin/TeighaFileConverter"
            if not os.path.exists(teigha):
                teigha = "/usr/bin/ODAFileConverter"
        elif platform.system() == "Windows":
            odadir = os.path.expandvars(r"D:\Program Files\ODA\ODAFileConverter_title 21.9.0\ODAFileConverter.exe")
            print(odadir)
            if os.path.exists(odadir):
                print("ok")
                subdirs = os.walk(odadir).next()[1]
                for sub in subdirs:
                    t = (odadir + os.sep + sub + os.sep
                         + "ODAFileConverter.exe")
                    t = os.path.join(odadir, sub, "ODAFileConverter.exe")
                    if os.path.exists(t):
                        teigha = t
    if teigha:
        if os.path.exists(teigha):
            return teigha
    # from DraftTools import translate
    # _msg = ("ODA (formerly Teigha) File Converter not found, "
    #         "DWG support is disabled")
    # FCC.PrintMessage(translate("draft", _msg) + "\n")
    return None


def convertToDxf(dwgfilename):
    """Convert a DWG file to a DXF file.
    If the converter is found it is used, otherwise the conversion fails.
    Parameters
    ----------
    dwgfilename : str
        The input filename.
    Returns
    -------
    str
        The new file produced.
    """
    
    global tmp_folder

    if shutil.which("dwg2dxf"):
        basename = os.path.basename(dwgfilename)
        result = tmp_folder + os.sep + os.path.splitext(basename)[0] + ".dxf"
        proc = subprocess.Popen(("dwg2dxf", dwgfilename, "-o", result))
        proc.communicate()
        return result
    teigha = getTeighaConverter()
    if teigha:
        indir = os.path.dirname(dwgfilename)
        
        basename = os.path.basename(dwgfilename)
        cmdline = ('"%s" "%s" "%s" "ACAD2010" "DXF" "0" "1" "%s"'
                   % (teigha, indir, tmp_folder, basename))
        print("cmd = " + cmdline)
        FCC.PrintMessage(translate("ImportDWG", "Converting: ")
                         + cmdline + "\n")
        if six.PY2:
            if isinstance(cmdline, six.text_type):
                encoding = sys.getfilesystemencoding()
                cmdline = cmdline.encode(encoding)
        subprocess.call(cmdline, shell=True)  # os.system(cmdline)
        result = tmp_folder + os.sep + os.path.splitext(basename)[0] + ".dxf"
        if os.path.exists(result):
            FCC.PrintMessage(translate("ImportDWG",
                                       "Conversion successful") + "\n")
            return result
        else:
            _msg = ("Error during DWG to DXF conversion. "
                    "Try moving the DWG file to a directory path\n"
                    "without spaces and non-english characters, "
                    "or try saving to a lower DWG version.")
            FCC.PrintMessage(translate("ImportDWG", _msg) + "\n")
    return None


def convertToDwg(dxffilename, dwgfilename):
    """Convert a DXF file to a DWG file.
    If the converter is found it is used, otherwise the conversion fails.
    Parameters
    ----------
    dxffilename : str
        The input DXF file
    dwgfilename : str
        The output DWG file
    Returns
    -------
    str
        The same `dwgfilename` file path.
    """
    
    if shutil.which("dxf2dwg"):
        proc = subprocess.Popen(("dxf2dwg", dxffilename, "-y", "-o", dwgfilename))
        proc.communicate()
        return dwgfilename

    teigha = getTeighaConverter()
    if teigha:
        indir = os.path.dirname(dxffilename)
        basename = os.path.basename(dxffilename)
        cmdline = ('"%s" "%s" "%s" "ACAD2000" "DWG" "0" "1" "%s"'
                   % (teigha, indir, tmp_folder, basename))
        FCC.PrintMessage(translate("ImportDWG", "Converting: ")
                         + cmdline + "\n")
        subprocess.call(cmdline, shell=True)  # os.system(cmdline)
        return dwgfilename
    return None


tmp_folder = os.environ.get('TEMP_FOLDER')
results_folder = os.environ.get('RESULTS_FOLDER')
search_folders = os.environ.get('SEARCH_FOLDERS').split('";"')
search_folders[0] = search_folders[0][1:]
search_folders[-1] = search_folders[-1][:-1]
last_date = os.environ.get('LAST_DATE')
oda_path = os.environ.get('ODA_PATH')

document_index = 0
for search_folder in search_folders:
    for root, dirs, files in os.walk(search_folder): 
        for file in files:     
            if file.endswith('.dwg'):                 
                try:
                    file_path = root + "\\" + file
                    mtime = os.path.getctime(file_path)
                    last_modified_date = datetime.fromtimestamp(mtime)
                    if last_modified_date > datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S'):
                        convertToDxf(file_path)
                        importDXF.open(tmp_folder + "\\" + file[:-3] + "dxf")                        
                        document = list(app.listDocuments().keys())[document_index]
                        document_index += 1
                        app.setActiveDocument(document)
                        app.ActiveDocument=app.getDocument(document)

                        gui.export(app.ActiveDocument.Objects, results_folder + "\\" + file[:-3] + "pdf")
                except OSError:                    
                    mtime = 0
dotenv.set_key(dotenv_path, "LAST_DATE", str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
