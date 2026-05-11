@echo off
setlocal enabledelayedexpansion

REM Hybrid Auditor EXE builder (Windows)
REM Safe for educational/authorized testing software distribution only.

where py >nul 2>nul
if %errorlevel%==0 (
  set "PY_CMD=py"
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    set "PY_CMD=python"
  ) else (
    echo [ERROR] Python not found in PATH. Install Python 3.10+ and check "Add python.exe to PATH".
    pause
    exit /b 1
  )
)

echo [INFO] Using !PY_CMD!
!PY_CMD! -m pip install --upgrade pip
if errorlevel 1 goto :fail

!PY_CMD! -m pip install -r requirements.txt
if errorlevel 1 goto :fail

!PY_CMD! -m pip install pyinstaller
if errorlevel 1 goto :fail

!PY_CMD! -m PyInstaller --noconfirm --clean --onefile --name HybridAuditor ^
  --add-data "templates;templates" ^
  --add-data "static;static" ^
  --add-data "translations;translations" ^
  --add-data "instance;instance" ^
  hybrid_launcher.py
if errorlevel 1 goto :fail

if exist dist\HybridAuditor.exe (
  echo [OK] Build completed: dist\HybridAuditor.exe
  echo [OK] Run and open http://127.0.0.1:5000
  pause
  exit /b 0
)

echo [ERROR] Build reported success but EXE not found.
pause
exit /b 1

:fail
echo [ERROR] Build failed. Scroll up and fix the first error.
echo [TIP] If OneDrive path causes issues, move project to C:\Projects\HybridAuditor and retry.
pause
exit /b 1
