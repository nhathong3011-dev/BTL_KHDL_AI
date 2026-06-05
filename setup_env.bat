@echo off
REM Tao moi truong fraud-aml-demo (khong can conda trong PATH)
set CONDA=C:\Users\DUC- PC\anaconda3\Scripts\conda.exe
cd /d "%~dp0"

echo === Kiem tra Anaconda ===
if not exist "%CONDA%" (
    echo Khong tim thay Anaconda tai: %CONDA%
    echo Hay sua duong dan CONDA trong file setup_env.bat
    pause
    exit /b 1
)

echo === Tao moi truong (neu chua co) ===
"%CONDA%" env list | findstr /C:"fraud-aml-demo" >nul
if errorlevel 1 (
    "%CONDA%" create -n fraud-aml-demo python=3.11 pip -y -c defaults
)

echo === Cai thu vien ===
"%CONDA%" run -n fraud-aml-demo pip install -r requirements.txt

echo.
echo === XONG ===
echo Chay web: run.bat
pause
