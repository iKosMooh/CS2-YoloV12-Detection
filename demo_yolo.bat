@echo off
REM CS2 YOLO Detection Demo - Educational Purpose
REM This script demonstrates real-time object detection using YOLOv12

echo ========================================
echo CS2 YOLOv12 Detection Demo
echo Educational Computer Vision Project
echo ========================================
echo.

REM Check if model exists
if exist "runs\train\weights\best.pt" (
    echo [OK] YOLOv12 model found
) else (
    echo [ERROR] Model not found!
    echo Please train the model first: start_training.bat
    echo.
    pause
    exit /b 1
)

echo [INFO] Checking dependencies...

REM Check for virtual environment
if exist "venv\Scripts\python.exe" (
    echo [INFO] Using virtual environment
    call venv\Scripts\activate.bat
    
    REM Install missing dependencies
    python -c "import win32gui" 2>nul
    if errorlevel 1 (
        echo [INFO] Installing pywin32...
        pip install pywin32 --quiet
    )
) else (
    echo [INFO] Using system Python
    
    REM Install missing dependencies
    python -c "import win32gui" 2>nul
    if errorlevel 1 (
        echo [INFO] Installing pywin32...
        pip install pywin32 --quiet
    )
)

echo.
echo [INFO] Starting real-time detection demo...
echo.
echo IMPORTANT: For best results, have CS2 running!
echo.
echo The demo will:
echo - Capture CS2 window (if found) or full screen
echo - Display detections in real-time
echo - Target 30+ FPS performance
echo.
echo Controls:
echo   Q - Quit demo
echo   S - Save screenshot
echo   C - Toggle class names
echo   R - Refresh CS2 window
echo.

if exist "venv\Scripts\python.exe" (
    venv\Scripts\python demo_detection.py
) else (
    python demo_detection.py
)

echo.
pause
