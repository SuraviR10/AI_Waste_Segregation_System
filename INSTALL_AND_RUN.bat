@echo off
echo Installing dependencies...
python -m pip install streamlit opencv-python pandas numpy pillow pyttsx3

echo.
echo Installation complete!
echo.
echo Starting application...
python -m streamlit run app.py

pause
