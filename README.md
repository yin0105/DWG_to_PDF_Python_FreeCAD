# DWG_to_PDF_python

Installing
---------------------------
1. Download <a href="https://github.com/FreeCAD/FreeCAD/releases">FreeCAD</a> and extract it.
2. Donwload <a href="https://www.opendesign.com/guestfiles/oda_file_converter">ODAFileConverter</a> and install it.
3. Install Python 3.8
4. Clone this project.
5. Run pip install -r requirements.txt
6. Copy "Lib\site-packages\dotenv" folder of python folder to "\bin\Lib\site-packages" of FreeCAD folder


Run
-------------------------------
1. Set SEARCH_FOLDERS(input folders with .dwg files), RESULTS_FOLDER(output folder where .pdf files will be saved) and TEMP_FOLDER in .env file.
2. Set the path of ODAFileConverter.exe in ODA_PATH variable of .env file
3. Run Command Prompt
4. Move to bin folder of FreeCAD folder.
5. Run following command as:
    freecad <path of project>\app.py
