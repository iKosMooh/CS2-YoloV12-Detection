"""
Test environment setup
"""
import sys
print(f"Python: {sys.version}")
print(f"Executable: {sys.executable}")
print()

print("Testing imports...")
print("-" * 50)

try:
    import torch
    print(f"✅ PyTorch: {torch.__version__}")
    print(f"   CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"   CUDA Version: {torch.version.cuda}")
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
except Exception as e:
    print(f"❌ PyTorch: {e}")

print()

try:
    import roboflow
    print(f"✅ Roboflow: {roboflow.__version__}")
except Exception as e:
    print(f"❌ Roboflow: {e}")

try:
    import supervision
    print(f"✅ Supervision: {supervision.__version__}")
except Exception as e:
    print(f"❌ Supervision: {e}")

try:
    import yaml
    print(f"✅ PyYAML: OK")
except Exception as e:
    print(f"❌ PyYAML: {e}")

try:
    import cv2
    print(f"✅ OpenCV: {cv2.__version__}")
except Exception as e:
    print(f"❌ OpenCV: {e}")

print()
print("Testing Ultralytics import...")
try:
    from ultralytics import YOLO
    print(f"✅ Ultralytics YOLO: OK")
except Exception as e:
    print(f"❌ Ultralytics: {e}")

print()
print("-" * 50)
print("Environment test complete!")
