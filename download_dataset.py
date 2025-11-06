"""
Download dataset from Roboflow
"""
import os
import yaml
from pathlib import Path
from roboflow import Roboflow

def load_config():
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def download_dataset():
    """Download dataset from Roboflow"""
    print("=" * 60)
    print("YOLOv12 Dataset Download")
    print("=" * 60)
    print()
    
    # Load config
    config = load_config()
    rf_config = config['roboflow']
    
    # Initialize Roboflow
    print(f"📡 Connecting to Roboflow...")
    rf = Roboflow(api_key=rf_config['api_key'])
    
    # Get project
    print(f"📦 Loading project: {rf_config['workspace']}/{rf_config['project']}")
    project = rf.workspace(rf_config['workspace']).project(rf_config['project'])
    
    # Get version
    version = project.version(rf_config['version'])
    
    # Create datasets directory
    datasets_dir = Path("./datasets")
    datasets_dir.mkdir(exist_ok=True)
    
    # Download dataset
    print(f"⬇️  Downloading dataset (version {rf_config['version']})...")
    os.chdir(str(datasets_dir))
    dataset = version.download("yolov8")  # YOLOv12 uses YOLOv8 format
    os.chdir("..")
    
    # Fix data.yaml for YOLOv12 compatibility
    print(f"🔧 Fixing data.yaml for YOLOv12...")
    data_yaml_path = Path(dataset.location) / "data.yaml"
    
    # Read current data.yaml
    with open(data_yaml_path, 'r') as f:
        lines = f.readlines()
    
    # Remove last 4 lines (old paths)
    lines = lines[:-4]
    
    # Add new paths (relative to data.yaml location)
    lines.append("test: test/images\n")
    lines.append("train: train/images\n")
    lines.append("val: valid/images\n")
    
    # Write back
    with open(data_yaml_path, 'w') as f:
        f.writelines(lines)
    
    print()
    print("✅ Dataset downloaded successfully!")
    print(f"📁 Location: {dataset.location}")
    print()
    
    # Print dataset info
    with open(data_yaml_path, 'r') as f:
        data_yaml = yaml.safe_load(f)
    
    print("📊 Dataset Information:")
    print(f"   Classes: {data_yaml['nc']}")
    print(f"   Names: {', '.join(data_yaml['names'])}")
    print()
    
    # Count images
    train_path = Path(dataset.location) / "train" / "images"
    valid_path = Path(dataset.location) / "valid" / "images"
    test_path = Path(dataset.location) / "test" / "images"
    
    train_count = len(list(train_path.glob("*"))) if train_path.exists() else 0
    valid_count = len(list(valid_path.glob("*"))) if valid_path.exists() else 0
    test_count = len(list(test_path.glob("*"))) if test_path.exists() else 0
    
    print("📈 Dataset Split:")
    print(f"   Train: {train_count} images")
    print(f"   Valid: {valid_count} images")
    print(f"   Test: {test_count} images")
    print()
    
    return dataset.location

if __name__ == "__main__":
    try:
        dataset_path = download_dataset()
        print("🎉 Ready to train! Run: python train.py")
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        print("\nPlease check:")
        print("1. Your Roboflow API key is correct in config.yaml")
        print("2. You have internet connection")
        print("3. The project workspace and name are correct")
