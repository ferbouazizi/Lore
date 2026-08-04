@echo off
call venv\Scripts\activate

if "%1"=="ui" (
    streamlit run app.py
) else (
    python main.py
)