"""
Monitor GPU usage during training
"""
import time
import psutil
import GPUtil
from datetime import datetime

def monitor_gpu(interval=2):
    """Monitor GPU usage in real-time"""
    print("=" * 70)
    print("GPU Monitor - Press Ctrl+C to stop")
    print("=" * 70)
    print()
    
    try:
        while True:
            # Clear screen (Windows)
            print("\033[H\033[J", end="")
            
            # Get timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"🕐 {timestamp}")
            print()
            
            # GPU Info
            gpus = GPUtil.getGPUs()
            if gpus:
                for i, gpu in enumerate(gpus):
                    print(f"🎮 GPU {i}: {gpu.name}")
                    print(f"   Temperature: {gpu.temperature}°C")
                    print(f"   Load: {gpu.load * 100:.1f}%")
                    print(f"   Memory: {gpu.memoryUsed:.0f}MB / {gpu.memoryTotal:.0f}MB ({gpu.memoryUtil * 100:.1f}%)")
                    print()
            else:
                print("❌ No GPU detected")
                print()
            
            # CPU Info
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            print(f"💻 CPU Usage: {cpu_percent}%")
            print(f"💾 RAM Usage: {memory.used / 1024**3:.1f}GB / {memory.total / 1024**3:.1f}GB ({memory.percent}%)")
            print()
            
            # Wait
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print()
        print("Monitor stopped")

if __name__ == "__main__":
    monitor_gpu()
