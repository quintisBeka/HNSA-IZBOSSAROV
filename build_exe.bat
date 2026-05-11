@echo off
REM Build standalone Windows executable for Hybrid Auditor
REM Usage: run this file on Windows where Python + pip are installed.

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

pyinstaller --noconfirm --onefile --name HybridAuditor ^
  --add-data "templates;templates" ^
  --add-data "static;static" ^
  --add-data "translations;translations" ^
  --add-data "instance;instance" ^
  hybrid_launcher.py

echo.
echo Build completed. EXE is in dist\HybridAuditor.exe
pause
