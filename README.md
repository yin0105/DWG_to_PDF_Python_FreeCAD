# DWG_to_PDF_python

Installing
---------------------------
1. Download <a href="https://github.com/FreeCAD/FreeCAD/releases">FreeCAD</a> and extract it.
2. Add paths lib and bin of FreeCAD into system path.
3. Donwload <a href="https://www.opendesign.com/guestfiles/oda_file_converter">ODAFileConverter</a> and install it.
4. Add path of ODAFileConverter into system path.
5. Install Python 3.8
6. Clone this project.
7. Run pip install -r requirements.txt
8. Copy "Lib\site-packages\dotenv" folder of python folder to "\bin\Lib\site-packages" of FreeCAD folder


Run
-------------------------------
1. Set SEARCH_FOLDERS(input folders with .dwg files) and RESULTS_FOLDER(output folder where .pdf files will be saved) in .env file .
2. Run Command Prompt
3. Move to bin folder of FreeCAD folder.
4. Run following command as:
    freecad <path of project>\app.py
