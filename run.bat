@echo off
REM Chay web demo — dung duong dan day du toi conda
set CONDA=C:\Users\DUC- PC\anaconda3\Scripts\conda.exe
cd /d "%~dp0"

if not exist "%CONDA%" (
    echo Khong tim thay Anaconda. Mo Anaconda Prompt hoac chay setup_env.bat
    pause
    exit /b 1
)

if not exist artifacts\models.joblib (
    echo Dang huan luyen mo hinh...
    "%CONDA%" run -n fraud-aml-demo python train.py
)

echo Mo web tai http://localhost:8501
"%CONDA%" run -n fraud-aml-demo streamlit run dashboard/app.py
