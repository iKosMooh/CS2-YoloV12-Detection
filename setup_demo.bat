@echo off
REM Quick Setup for CS2 YOLOv12 Detection Demo

echo ========================================
echo CS2 YOLOv12 Detection - Demo Setup
echo ========================================
echo.

REM Check Python version
python --version 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo [INFO] Checking for virtual environment...
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [INFO] Virtual environment created!
) else (
    echo [INFO] Virtual environment already exists
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

echo [INFO] Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Dependencies installed:
echo - YOLOv12 (Ultralytics)
echo - OpenCV (opencv-contrib-python)
echo - MSS (Screen Capture)
echo - NumPy
echo.
echo Next steps:
echo 1. Ensure you have a trained model at: runs\train\weights\best.pt
echo 2. Run the demo: demo_yolo.bat
echo.
echo Controls in demo:
echo   Q - Quit
echo   S - Save screenshot
echo   C - Toggle confidence threshold
echo.

pause
