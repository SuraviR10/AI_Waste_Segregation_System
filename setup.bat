@echo off
echo ========================================
echo AI Waste Segregation System - Setup
echo ========================================
echo.

echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)
echo.

echo [2/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo [3/3] Setup complete!
echo.
echo ========================================
echo Ready to run!
echo ========================================
echo.
echo To start the application, run:
echo   run.bat
echo.
echo Or manually run:
echo   streamlit run app.py
echo.
pause
