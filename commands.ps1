# PowerShell Quick Commands

# ============================================
# YOLOv12 Training Environment
# Quick Commands for PowerShell
# ============================================

# CHECK ENVIRONMENT
# ----------------

# Check Python version
function Check-Python {
    python --version
    Write-Host "`nPython location:" -ForegroundColor Cyan
    python -c "import sys; print(sys.executable)"
}

# Check CUDA
function Check-CUDA {
    Write-Host "Checking CUDA..." -ForegroundColor Cyan
    nvidia-smi
}

# Check PyTorch
function Check-PyTorch {
    Write-Host "Checking PyTorch..." -ForegroundColor Cyan
    python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'CUDA Version: {torch.version.cuda}' if torch.cuda.is_available() else 'No CUDA')"
}

# Check all
function Check-All {
    Write-Host "==================================" -ForegroundColor Green
    Write-Host "Environment Check" -ForegroundColor Green
    Write-Host "==================================" -ForegroundColor Green
    Write-Host ""
    Check-Python
    Write-Host ""
    Check-CUDA
    Write-Host ""
    Check-PyTorch
}

# SETUP
# -----

# Full setup
function Setup-Environment {
    Write-Host "Setting up YOLOv12 environment..." -ForegroundColor Cyan
    .\setup.bat
}

# Install PyTorch only
function Install-PyTorch {
    Write-Host "Installing PyTorch with CUDA 12.9..." -ForegroundColor Cyan
    pip install torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu129
}

# Clone YOLOv12
function Clone-YOLOv12 {
    if (Test-Path "yolov12") {
        Write-Host "YOLOv12 already exists, pulling updates..." -ForegroundColor Yellow
        cd yolov12
        git pull
        cd ..
    } else {
        Write-Host "Cloning YOLOv12..." -ForegroundColor Cyan
        git clone https://github.com/sunsmarterjie/yolov12
    }
}

# DATASET
# -------

# Download dataset
function Download-Dataset {
    Write-Host "Downloading dataset from Roboflow..." -ForegroundColor Cyan
    python download_dataset.py
}

# Check dataset
function Check-Dataset {
    if (Test-Path "datasets") {
        Write-Host "Dataset folder found!" -ForegroundColor Green
        $yamls = Get-ChildItem -Path datasets -Filter "data.yaml" -Recurse
        if ($yamls) {
            Write-Host "data.yaml files:" -ForegroundColor Cyan
            $yamls | ForEach-Object { Write-Host "  - $($_.FullName)" }
        }
    } else {
        Write-Host "No dataset found! Run: Download-Dataset" -ForegroundColor Red
    }
}

# TRAINING
# --------

# Start training
function Start-Training {
    Write-Host "Starting training..." -ForegroundColor Cyan
    python train.py
}

# Resume training
function Resume-Training {
    Write-Host "Resuming training..." -ForegroundColor Cyan
    python train.py
}

# Quick start (all-in-one)
function Quick-Start {
    Write-Host "Quick Start: Setup + Download + Train" -ForegroundColor Green
    .\start_training.bat
}

# VALIDATION & TESTING
# --------------------

# Validate model
function Validate-Model {
    Write-Host "Validating model..." -ForegroundColor Cyan
    python validate.py
}

# Run inference
function Test-Model {
    Write-Host "Running inference..." -ForegroundColor Cyan
    python inference.py
}

# Benchmark
function Benchmark-Model {
    Write-Host "Benchmarking model..." -ForegroundColor Cyan
    python benchmark.py
}

# MONITORING
# ----------

# Monitor GPU
function Monitor-GPU {
    Write-Host "Starting GPU monitor (Ctrl+C to stop)..." -ForegroundColor Cyan
    python monitor_gpu.py
}

# Watch GPU with nvidia-smi
function Watch-GPU {
    Write-Host "Watching GPU with nvidia-smi (Ctrl+C to stop)..." -ForegroundColor Cyan
    while ($true) {
        Clear-Host
        nvidia-smi
        Start-Sleep -Seconds 1
    }
}

# EXPORT
# ------

# Export model
function Export-Model {
    Write-Host "Exporting model..." -ForegroundColor Cyan
    python export_model.py
}

# RESULTS
# -------

# Show results
function Show-Results {
    $trainDir = "runs\detect\train"
    if (Test-Path $trainDir) {
        Write-Host "Training results found!" -ForegroundColor Green
        Write-Host "`nResults folder: $trainDir" -ForegroundColor Cyan
        
        # List key files
        $keyFiles = @(
            "weights\best.pt",
            "weights\last.pt",
            "confusion_matrix.png",
            "results.png",
            "results.csv"
        )
        
        Write-Host "`nKey files:" -ForegroundColor Cyan
        foreach ($file in $keyFiles) {
            $fullPath = Join-Path $trainDir $file
            if (Test-Path $fullPath) {
                $size = (Get-Item $fullPath).Length / 1MB
                Write-Host "  ✓ $file ($([math]::Round($size, 2)) MB)" -ForegroundColor Green
            } else {
                Write-Host "  ✗ $file (not found)" -ForegroundColor Red
            }
        }
        
        # Open folder
        Write-Host "`nOpen results folder? (Y/N)" -ForegroundColor Yellow
        $response = Read-Host
        if ($response -eq 'Y' -or $response -eq 'y') {
            Start-Process $trainDir
        }
    } else {
        Write-Host "No training results found!" -ForegroundColor Red
        Write-Host "Train a model first: Start-Training" -ForegroundColor Yellow
    }
}

# Open results folder
function Open-Results {
    $trainDir = "runs\detect\train"
    if (Test-Path $trainDir) {
        Start-Process $trainDir
    } else {
        Write-Host "No results folder found!" -ForegroundColor Red
    }
}

# UTILITIES
# ---------

# Clean cache
function Clear-Cache {
    Write-Host "Clearing cache..." -ForegroundColor Cyan
    if (Test-Path "cache") {
        Remove-Item -Path "cache\*" -Recurse -Force
        Write-Host "Cache cleared!" -ForegroundColor Green
    } else {
        Write-Host "No cache folder found." -ForegroundColor Yellow
    }
}

# Clean runs
function Clear-Runs {
    Write-Host "⚠️  This will delete all training results!" -ForegroundColor Red
    Write-Host "Are you sure? (Y/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq 'Y' -or $response -eq 'y') {
        if (Test-Path "runs") {
            Remove-Item -Path "runs" -Recurse -Force
            Write-Host "Runs folder cleared!" -ForegroundColor Green
        }
    }
}

# List all commands
function Show-Commands {
    Write-Host "==================================" -ForegroundColor Green
    Write-Host "YOLOv12 PowerShell Commands" -ForegroundColor Green
    Write-Host "==================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "SETUP:" -ForegroundColor Cyan
    Write-Host "  Setup-Environment    - Full setup"
    Write-Host "  Install-PyTorch      - Install PyTorch only"
    Write-Host "  Clone-YOLOv12        - Clone YOLOv12 repo"
    Write-Host ""
    Write-Host "CHECK:" -ForegroundColor Cyan
    Write-Host "  Check-Python         - Check Python"
    Write-Host "  Check-CUDA           - Check CUDA"
    Write-Host "  Check-PyTorch        - Check PyTorch"
    Write-Host "  Check-All            - Check everything"
    Write-Host ""
    Write-Host "DATASET:" -ForegroundColor Cyan
    Write-Host "  Download-Dataset     - Download from Roboflow"
    Write-Host "  Check-Dataset        - Check dataset"
    Write-Host ""
    Write-Host "TRAINING:" -ForegroundColor Cyan
    Write-Host "  Start-Training       - Start training"
    Write-Host "  Resume-Training      - Resume training"
    Write-Host "  Quick-Start          - All-in-one setup + train"
    Write-Host ""
    Write-Host "TESTING:" -ForegroundColor Cyan
    Write-Host "  Validate-Model       - Validate on test set"
    Write-Host "  Test-Model           - Run inference"
    Write-Host "  Benchmark-Model      - Benchmark performance"
    Write-Host ""
    Write-Host "MONITORING:" -ForegroundColor Cyan
    Write-Host "  Monitor-GPU          - Monitor with script"
    Write-Host "  Watch-GPU            - Watch with nvidia-smi"
    Write-Host ""
    Write-Host "RESULTS:" -ForegroundColor Cyan
    Write-Host "  Show-Results         - Show results summary"
    Write-Host "  Open-Results         - Open results folder"
    Write-Host ""
    Write-Host "EXPORT:" -ForegroundColor Cyan
    Write-Host "  Export-Model         - Export to ONNX/TensorRT/etc"
    Write-Host ""
    Write-Host "UTILITIES:" -ForegroundColor Cyan
    Write-Host "  Clear-Cache          - Clear image cache"
    Write-Host "  Clear-Runs           - Clear all results"
    Write-Host "  Show-Commands        - Show this help"
    Write-Host ""
    Write-Host "==================================" -ForegroundColor Green
}

# Show help on load
Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "YOLOv12 Training Environment" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "Type 'Show-Commands' to see all available commands" -ForegroundColor Cyan
Write-Host ""
Write-Host "Quick Start:" -ForegroundColor Yellow
Write-Host "  1. Setup-Environment" -ForegroundColor White
Write-Host "  2. Download-Dataset" -ForegroundColor White
Write-Host "  3. Start-Training" -ForegroundColor White
Write-Host ""
