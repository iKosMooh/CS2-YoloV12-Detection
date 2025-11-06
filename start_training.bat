@echo off
echo ============================================
echo Quick Start - YOLOv12 Training
echo ============================================
echo.

REM Check if setup was done
if not exist "yolov12" (
    echo Setting up environment...
    call setup.bat
)

REM Check if dataset exists
if not exist "datasets" (
    echo Downloading dataset...
    python download_dataset.py
    echo.
)

echo Starting training...
echo.
python train.py

pause
