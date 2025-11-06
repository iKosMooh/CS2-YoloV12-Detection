"""
YOLOv12 Training Script with Resume and Cache Support
Optimized for RTX GPU with 6GB VRAM
"""
import os
import sys
import yaml
import torch
from pathlib import Path
import psutil
import GPUtil

# Add YOLOv12 to path
yolov12_path = Path(__file__).parent / "yolov12"
if yolov12_path.exists():
    sys.path.insert(0, str(yolov12_path))

from ultralytics import YOLO

def load_config():
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def check_gpu():
    """Check GPU availability and memory"""
    if not torch.cuda.is_available():
        print("❌ CUDA is not available. Training requires a GPU.")
        return False
    
    print("🎮 GPU Information:")
    print(f"   Device: {torch.cuda.get_device_name(0)}")
    print(f"   CUDA Version: {torch.version.cuda}")
    print(f"   PyTorch Version: {torch.__version__}")
    
    gpus = GPUtil.getGPUs()
    if gpus:
        gpu = gpus[0]
        print(f"   Total Memory: {gpu.memoryTotal} MB")
        print(f"   Free Memory: {gpu.memoryFree} MB")
        print(f"   Used Memory: {gpu.memoryUsed} MB")
        
        # Check if we have enough memory
        if gpu.memoryTotal < 5000:  # Less than 5GB
            print("\n⚠️  Warning: Your GPU has less than 5GB memory.")
            print("   Consider reducing batch_size in config.yaml")
    
    print()
    return True

def setup_directories(config):
    """Create necessary directories"""
    paths = config['paths']
    for path_key, path_value in paths.items():
        Path(path_value).mkdir(parents=True, exist_ok=True)

def find_latest_checkpoint(runs_dir):
    """Find the latest checkpoint to resume from"""
    runs_path = Path(runs_dir) / "detect"
    if not runs_path.exists():
        return None
    
    # Find all training runs
    train_dirs = sorted(runs_path.glob("train*"))
    if not train_dirs:
        return None
    
    # Get latest run
    latest_run = train_dirs[-1]
    
    # Check for last.pt (checkpoint)
    checkpoint = latest_run / "weights" / "last.pt"
    if checkpoint.exists():
        return str(checkpoint)
    
    return None

def get_dataset_path():
    """Get dataset path"""
    # Look for downloaded dataset
    datasets_dir = Path("./datasets")
    if not datasets_dir.exists():
        print("❌ Dataset directory not found!")
        print("   Please run: python download_dataset.py")
        return None
    
    # Find data.yaml in downloaded dataset
    data_yamls = list(datasets_dir.glob("*/data.yaml"))
    if not data_yamls:
        print("❌ No dataset found!")
        print("   Please run: python download_dataset.py")
        return None
    
    return str(data_yamls[0])

def train():
    """Main training function"""
    print("=" * 70)
    print("YOLOv12 Object Detection Training")
    print("Optimized for RTX GPU with 6GB VRAM")
    print("=" * 70)
    print()
    
    # Load configuration
    config = load_config()
    train_config = config['training']
    gpu_config = config['gpu']
    
    # Check GPU
    if not check_gpu():
        return
    
    # Setup directories
    setup_directories(config)
    
    # Get dataset path
    data_path = get_dataset_path()
    if not data_path:
        return
    
    print(f"📊 Dataset: {data_path}")
    print()
    
    # Check for existing checkpoint
    checkpoint_path = None
    if train_config['resume']:
        checkpoint_path = find_latest_checkpoint(config['paths']['runs'])
        if checkpoint_path:
            print(f"♻️  Found checkpoint: {checkpoint_path}")
            print(f"   Resuming training from previous run...")
            print()
    
    # Initialize model
    print("🤖 Initializing model...")
    if checkpoint_path:
        # Resume from checkpoint
        model = YOLO(checkpoint_path)
        print(f"   Loaded checkpoint: {Path(checkpoint_path).name}")
    else:
        # Start fresh training
        model = YOLO(config['model']['checkpoint'])
        print(f"   Model: {config['model']['checkpoint']}")
    
    print()
    
    # Configure training parameters
    print("⚙️  Training Configuration:")
    print(f"   Epochs: {train_config['epochs']}")
    print(f"   Batch Size: {train_config['batch_size']}")
    print(f"   Image Size: {train_config['imgsz']}")
    print(f"   Device: GPU {train_config['device']}")
    print(f"   Cache: {train_config['cache']}")
    print(f"   AMP: {train_config['amp']}")
    print(f"   Workers: {train_config['workers']}")
    print()
    
    # GPU Memory settings
    print("💾 GPU Memory Configuration:")
    print(f"   Target VRAM Usage: {gpu_config['min_memory_gb']}-{gpu_config['max_memory_gb']} GB")
    print()
    
    # Set memory fraction
    torch.cuda.set_per_process_memory_fraction(
        gpu_config['max_memory_gb'] / 8.0,  # Assuming 8GB max
        device=train_config['device']
    )
    
    print("🚀 Starting training...")
    print("   Press Ctrl+C to stop (checkpoint will be saved)")
    print()
    print("-" * 70)
    print()
    
    try:
        # Train the model
        results = model.train(
            data=data_path,
            epochs=train_config['epochs'],
            batch=train_config['batch_size'],
            imgsz=train_config['imgsz'],
            device=train_config['device'],
            workers=train_config['workers'],
            cache=train_config['cache'],
            optimizer=train_config['optimizer'],
            lr0=train_config['lr0'],
            lrf=train_config['lrf'],
            momentum=train_config['momentum'],
            weight_decay=train_config['weight_decay'],
            hsv_h=train_config['hsv_h'],
            hsv_s=train_config['hsv_s'],
            hsv_v=train_config['hsv_v'],
            degrees=train_config['degrees'],
            translate=train_config['translate'],
            scale=train_config['scale'],
            shear=train_config['shear'],
            perspective=train_config['perspective'],
            flipud=train_config['flipud'],
            fliplr=train_config['fliplr'],
            mosaic=train_config['mosaic'],
            mixup=train_config['mixup'],
            copy_paste=train_config['copy_paste'],
            val=train_config['val'],
            save_period=train_config['save_period'],
            amp=train_config['amp'],
            patience=train_config['patience'],
            project=config['paths']['runs'],
            name='train',
            exist_ok=True,
            resume=checkpoint_path is not None
        )
        
        print()
        print("=" * 70)
        print("✅ Training completed successfully!")
        print("=" * 70)
        print()
        
        # Print results location
        save_dir = Path(config['paths']['runs']) / "detect" / "train"
        print(f"📁 Results saved to: {save_dir}")
        print()
        print("📊 View results:")
        print(f"   - Weights: {save_dir / 'weights'}")
        print(f"   - Confusion Matrix: {save_dir / 'confusion_matrix.png'}")
        print(f"   - Training Curves: {save_dir / 'results.png'}")
        print()
        print("🎯 Best model saved at:")
        print(f"   {save_dir / 'weights' / 'best.pt'}")
        print()
        
    except KeyboardInterrupt:
        print()
        print("⚠️  Training interrupted by user")
        print("   Checkpoint saved. Run again to resume training.")
        print()
    except Exception as e:
        print()
        print(f"❌ Training error: {e}")
        print()
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Check if dataset exists
    datasets_dir = Path("./datasets")
    if not datasets_dir.exists() or not list(datasets_dir.glob("*/data.yaml")):
        print("⚠️  No dataset found!")
        print()
        response = input("Would you like to download the dataset now? (y/n): ")
        if response.lower() == 'y':
            print()
            os.system("python download_dataset.py")
            print()
            input("Press Enter to start training...")
            print()
    
    train()
