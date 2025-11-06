"""
Validate trained model on test set
"""
import sys
import yaml
from pathlib import Path
import supervision as sv

# Add YOLOv12 to path
yolov12_path = Path(__file__).parent / "yolov12"
if yolov12_path.exists():
    sys.path.insert(0, str(yolov12_path))

from ultralytics import YOLO

def load_config():
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def find_best_weights():
    """Find the best trained model weights"""
    config = load_config()
    runs_dir = Path(config['paths']['runs']) / "detect"
    
    if not runs_dir.exists():
        print("❌ No trained model found!")
        return None
    
    train_dirs = sorted(runs_dir.glob("train*"))
    if not train_dirs:
        return None
    
    latest_run = train_dirs[-1]
    best_weights = latest_run / "weights" / "best.pt"
    
    if best_weights.exists():
        return str(best_weights)
    
    return None

def get_dataset_path():
    """Get dataset path"""
    datasets_dir = Path("./datasets")
    if not datasets_dir.exists():
        return None
    
    data_yamls = list(datasets_dir.glob("*/data.yaml"))
    if not data_yamls:
        return None
    
    return str(data_yamls[0])

def validate_model():
    """Validate model on test set"""
    print("=" * 70)
    print("YOLOv12 Model Validation")
    print("=" * 70)
    print()
    
    # Find model
    weights_path = find_best_weights()
    if not weights_path:
        print("❌ No trained model found!")
        print("   Please train a model first: python train.py")
        return
    
    print(f"🤖 Loading model: {weights_path}")
    model = YOLO(weights_path)
    print("✅ Model loaded successfully!")
    print()
    
    # Get dataset
    data_path = get_dataset_path()
    if not data_path:
        print("❌ No dataset found!")
        return
    
    print(f"📊 Dataset: {data_path}")
    print()
    
    # Validate
    print("🔍 Running validation...")
    print()
    
    results = model.val(data=data_path)
    
    print()
    print("=" * 70)
    print("✅ Validation Results")
    print("=" * 70)
    print()
    
    # Print metrics
    print(f"📈 Metrics:")
    print(f"   mAP50: {results.box.map50:.4f}")
    print(f"   mAP50-95: {results.box.map:.4f}")
    print(f"   Precision: {results.box.mp:.4f}")
    print(f"   Recall: {results.box.mr:.4f}")
    print()
    
    # Per-class metrics
    print(f"📊 Per-Class Metrics:")
    for i, (name, ap) in enumerate(zip(results.names.values(), results.box.ap)):
        print(f"   {name}: AP={ap:.4f}")
    print()

if __name__ == "__main__":
    validate_model()
