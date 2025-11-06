@echo off
echo ============================================
echo YOLOv12 Training Environment Setup
echo ============================================
echo.

REM Check Python version
python --version
echo.

echo [1/5] Installing PyTorch with CUDA 12.9...
pip install torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu129
echo.

echo [2/5] Cloning YOLOv12 repository...
if not exist "yolov12" (
    git clone https://github.com/sunsmarterjie/yolov12
) else (
    echo YOLOv12 already cloned, pulling latest changes...
    cd yolov12
    git pull
    cd ..
)
echo.

echo [3/5] Installing YOLOv12 requirements...
cd yolov12
pip install -r requirements.txt
pip install -e .
cd ..
echo.

echo [4/5] Installing additional dependencies...
pip install -r requirements.txt
echo.

echo [5/5] Installing FlashAttention (this may take a while)...
pip install flash-attn --no-build-isolation
echo.

echo ============================================
echo Setup complete!
echo ============================================
echo.
echo Next steps:
echo 1. Configure your Roboflow API key in config.yaml
echo 2. Run: python download_dataset.py
echo 3. Run: python train.py
echo.
pause
