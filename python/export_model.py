"""
Export trained YOLOv12 model to different formats
Supports: ONNX, TensorRT, CoreML, TFLite, etc.
"""
import sys
from pathlib import Path
import yaml

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
        return None
    
    train_dirs = sorted(runs_dir.glob("train*"))
    if not train_dirs:
        return None
    
    latest_run = train_dirs[-1]
    best_weights = latest_run / "weights" / "best.pt"
    
    if best_weights.exists():
        return str(best_weights)
    
    return None

def export_model():
    """Export model to different formats"""
    print("=" * 70)
    print("YOLOv12 Model Export")
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
    
    # Show export options
    print("📦 Export Formats:")
    print("   1. ONNX       - Universal format (CPU/GPU)")
    print("   2. TensorRT   - NVIDIA GPU optimization")
    print("   3. OpenVINO   - Intel CPU/GPU optimization")
    print("   4. CoreML     - Apple devices (iOS/macOS)")
    print("   5. TFLite     - Mobile devices (Android/iOS)")
    print("   6. TF         - TensorFlow SavedModel")
    print("   7. All        - Export all formats")
    print()
    
    choice = input("Select format (1-7): ").strip()
    print()
    
    export_formats = {
        '1': ('onnx', 'ONNX'),
        '2': ('engine', 'TensorRT'),
        '3': ('openvino', 'OpenVINO'),
        '4': ('coreml', 'CoreML'),
        '5': ('tflite', 'TFLite'),
        '6': ('saved_model', 'TensorFlow'),
        '7': ('all', 'All Formats')
    }
    
    if choice not in export_formats:
        print("❌ Invalid choice!")
        return
    
    format_key, format_name = export_formats[choice]
    
    print(f"🔄 Exporting to {format_name}...")
    print("   This may take a few minutes...")
    print()
    
    try:
        if choice == '7':
            # Export all formats
            formats = ['onnx', 'engine', 'openvino', 'coreml', 'tflite', 'saved_model']
            for fmt in formats:
                print(f"📦 Exporting {fmt}...")
                try:
                    model.export(format=fmt, simplify=True)
                    print(f"✅ {fmt} exported successfully!")
                except Exception as e:
                    print(f"⚠️  {fmt} export failed: {e}")
                print()
        else:
            # Export single format
            model.export(format=format_key, simplify=True)
        
        print()
        print("=" * 70)
        print("✅ Export completed!")
        print("=" * 70)
        print()
        
        # Show exported files
        weights_dir = Path(weights_path).parent
        print(f"📁 Exported files in: {weights_dir}")
        print()
        print("📦 Files:")
        for file in sorted(weights_dir.glob("best.*")):
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"   {file.name} ({size_mb:.1f} MB)")
        print()
        
        # Usage instructions
        print("💡 Usage:")
        if choice == '1' or choice == '7':
            print("   ONNX: Use with ONNX Runtime, OpenCV DNN, etc.")
            print("   Example: cv2.dnn.readNetFromONNX('best.onnx')")
        if choice == '2' or choice == '7':
            print("   TensorRT: Use with TensorRT on NVIDIA GPUs")
            print("   Example: model = YOLO('best.engine')")
        if choice == '5' or choice == '7':
            print("   TFLite: Use on mobile devices")
            print("   Example: Load in Android/iOS app")
        print()
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        print()
        import traceback
        traceback.print_exc()

def main():
    """Main export function"""
    export_model()

if __name__ == "__main__":
    main()
