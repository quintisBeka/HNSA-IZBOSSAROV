@echo off
setlocal enabledelayedexpansion

REM Hybrid Auditor EXE builder (Windows)

set "PY_CMD="
call :find_python
if not defined PY_CMD (
  echo [WARN] Python not found in PATH.
  echo [INFO] Trying to install Python via winget...
  where winget >nul 2>nul
  if errorlevel 1 (
    echo [ERROR] winget is unavailable.
    echo [ACTION] Install Python manually from https://www.python.org/downloads/windows/
    echo [ACTION] IMPORTANT: enable "Add python.exe to PATH" during setup.
    pause
    exit /b 1
  )

  winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
  if errorlevel 1 (
    echo [ERROR] Automatic Python install failed.
    echo [ACTION] Install Python manually and rerun build_exe.bat.
    pause
    exit /b 1
  )

  call :find_python
  if not defined PY_CMD (
    echo [ERROR] Python still not detected after installation.
    echo [TIP] Restart CMD and run build_exe.bat again.
    pause
    exit /b 1
  )
)

echo [INFO] Using !PY_CMD!
!PY_CMD! -m pip install --upgrade pip || goto :fail
!PY_CMD! -m pip install -r requirements.txt || goto :fail
!PY_CMD! -m pip install pyinstaller || goto :fail

!PY_CMD! -m PyInstaller --noconfirm --clean --onefile --name HybridAuditor ^
  --add-data "templates;templates" ^
  --add-data "static;static" ^
  --add-data "translations;translations" ^
  --add-data "instance;instance" ^
  hybrid_launcher.py || goto :fail

if exist dist\HybridAuditor.exe (
  echo [OK] Build completed: dist\HybridAuditor.exe
  echo [OK] Run EXE and open http://127.0.0.1:5000
  pause
  exit /b 0
)

echo [ERROR] Build finished but dist\HybridAuditor.exe not found.
pause
exit /b 1

:find_python
where py >nul 2>nul
if %errorlevel%==0 (
  set "PY_CMD=py"
  exit /b 0
)
where python >nul 2>nul
if %errorlevel%==0 (
  set "PY_CMD=python"
  exit /b 0
)
exit /b 0

:fail
echo [ERROR] Build failed. Check first error above.
echo [TIP] If project is in OneDrive, move to C:\Projects\HybridAuditor and retry.
pause
exit /b 1
