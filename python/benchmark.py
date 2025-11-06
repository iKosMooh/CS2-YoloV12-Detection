"""
Benchmark trained model performance
Tests: Speed, FPS, Memory usage
"""
import sys
import time
import torch
import cv2
import numpy as np
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

def benchmark_model():
    """Benchmark model performance"""
    print("=" * 70)
    print("YOLOv12 Model Benchmark")
    print("=" * 70)
    print()
    
    # Find model
    weights_path = find_best_weights()
    if not weights_path:
        print("❌ No trained model found!")
        return
    
    print(f"🤖 Loading model: {weights_path}")
    model = YOLO(weights_path)
    print("✅ Model loaded successfully!")
    print()
    
    # Check CUDA
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"🎮 Device: {device.upper()}")
    if device == 'cuda':
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
    print()
    
    # Test parameters
    image_sizes = [640, 512, 416, 320]
    num_warmup = 10
    num_runs = 100
    
    print(f"🔧 Benchmark Settings:")
    print(f"   Warmup runs: {num_warmup}")
    print(f"   Test runs: {num_runs}")
    print()
    
    # Results storage
    results = []
    
    for imgsz in image_sizes:
        print(f"📊 Testing image size: {imgsz}x{imgsz}")
        print("-" * 50)
        
        # Create dummy image
        dummy_image = np.random.randint(0, 255, (imgsz, imgsz, 3), dtype=np.uint8)
        
        # Warmup
        print(f"   Warming up...")
        for _ in range(num_warmup):
            _ = model(dummy_image, verbose=False)
        
        if device == 'cuda':
            torch.cuda.synchronize()
        
        # Benchmark
        print(f"   Running benchmark...")
        times = []
        
        for i in range(num_runs):
            start = time.time()
            _ = model(dummy_image, verbose=False)
            
            if device == 'cuda':
                torch.cuda.synchronize()
            
            end = time.time()
            times.append(end - start)
            
            if (i + 1) % 20 == 0:
                print(f"   Progress: {i+1}/{num_runs}")
        
        # Calculate statistics
        times = np.array(times) * 1000  # Convert to ms
        mean_time = np.mean(times)
        std_time = np.std(times)
        min_time = np.min(times)
        max_time = np.max(times)
        fps = 1000 / mean_time
        
        results.append({
            'size': imgsz,
            'mean': mean_time,
            'std': std_time,
            'min': min_time,
            'max': max_time,
            'fps': fps
        })
        
        print()
        print(f"   Mean time: {mean_time:.2f}ms ± {std_time:.2f}ms")
        print(f"   Min time: {min_time:.2f}ms")
        print(f"   Max time: {max_time:.2f}ms")
        print(f"   FPS: {fps:.1f}")
        print()
    
    # Summary
    print("=" * 70)
    print("📊 Benchmark Summary")
    print("=" * 70)
    print()
    print(f"{'Size':<10} {'Mean (ms)':<15} {'Std (ms)':<15} {'FPS':<10}")
    print("-" * 70)
    
    for result in results:
        print(f"{result['size']}x{result['size']:<6} "
              f"{result['mean']:<15.2f} "
              f"{result['std']:<15.2f} "
              f"{result['fps']:<10.1f}")
    
    print()
    print("💡 Recommendations:")
    print()
    
    # Find best for different use cases
    fastest = max(results, key=lambda x: x['fps'])
    print(f"   Real-time (30+ FPS): {fastest['size']}x{fastest['size']} ({fastest['fps']:.1f} FPS)")
    
    balanced = results[0] if results[0]['fps'] >= 20 else results[1] if len(results) > 1 else results[0]
    print(f"   Balanced: {balanced['size']}x{balanced['size']} ({balanced['fps']:.1f} FPS)")
    
    accurate = results[0]
    print(f"   Accuracy: {accurate['size']}x{accurate['size']} ({accurate['fps']:.1f} FPS)")
    print()
    
    # Memory info
    if device == 'cuda':
        print("💾 GPU Memory:")
        print(f"   Allocated: {torch.cuda.memory_allocated() / 1024**2:.1f} MB")
        print(f"   Reserved: {torch.cuda.memory_reserved() / 1024**2:.1f} MB")
        print()

if __name__ == "__main__":
    benchmark_model()
