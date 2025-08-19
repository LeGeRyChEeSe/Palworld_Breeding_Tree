@echo off
cd /d "%~dp0"
call ./venv/Scripts/activate.bat

REM Récupérer la version dynamiquement
python core/scripts/get_version.py > version.tmp
set /p VERSION=<version.tmp
del version.tmp
echo Building version: %VERSION%

pyinstaller --onefile --clean ^
--noconsole ^
--distpath "Build" ^
--specpath ".Building" ^
--name "Palworld_Breeding_Tree-%VERSION%-Windows" ^
--icon "%~dp0Icons\icon.ico" ^
--workpath ".Building" ^
--collect-all graphviz ^
--hidden-import="graphviz._defaults" ^
--hidden-import="graphviz.backend" ^
--hidden-import="graphviz.dot" ^
--add-data "%~dp0Graphviz;Graphviz" ^
--add-data "%~dp0languages;languages" ^
--add-data "%~dp0Icons;Icons" ^
--add-data "%~dp0pals.json;." ^
Main.py