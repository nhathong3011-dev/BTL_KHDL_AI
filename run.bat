@echo off
cd /d "%~dp0"
call conda activate fraud-aml-demo
if errorlevel 1 (
    echo Tao moi truong: conda env create -f environment.yml
    conda env create -f environment.yml
    call conda activate fraud-aml-demo
)
if not exist artifacts\models.joblib (
    echo Dang huan luyen mo hinh...
    python train.py
)
streamlit run dashboard/app.py
