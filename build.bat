@echo off
cd /d "%~dp0"

call venv\Scripts\activate

pip install -r requirements.txt

rmdir /s /q build dist
del /q main.spec

pyinstaller ^
    --onefile ^
    --noconsole ^
    --add-data "assets;assets" ^
    --add-data "data;data" ^
    --hidden-import=blockblast ^
    --hidden-import=pygame ^
    --hidden-import=utils ^
    --name ELEKTRIS ^
    main.py

deactivate