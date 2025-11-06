"""
CS2 YOLO Detection Demo - Educational Purpose
Real-time object detection demonstration using YOLOv12

This script demonstrates:
- CS2.exe process window capture
- YOLOv12 object detection
- OpenCV visualization
- FPS monitoring (24+ FPS optimized)

Classes detected: CT, CT_head, T, T_head
"""

import cv2
import numpy as np
import mss
from pathlib import Path
from ultralytics import YOLO
import time
import sys
import psutil
import win32gui
import win32process

def find_cs2_process():
    """Find CS2.exe process and return PID"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() == 'cs2.exe':
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def find_window_by_pid(pid):
    """Find window handle by process ID"""
    result = []
    
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid == pid:
                result.append(hwnd)
        return True
    
    win32gui.EnumWindows(callback, None)
    
    # Return the main window (usually the first visible one)
    return result[0] if result else None

def get_window_rect_for_mss(hwnd):
    """Get window rectangle for MSS capture - captures full client area"""
    try:
        # Get window position
        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect
        
        # Get client area size (actual game rendering area)
        client_rect = win32gui.GetClientRect(hwnd)
        client_width = client_rect[2] - client_rect[0]
        client_height = client_rect[3] - client_rect[1]
        
        # Calculate window borders
        window_width = right - left
        window_height = bottom - top
        
        border_left = (window_width - client_width) // 2
        border_top = window_height - client_height - border_left
        
        return {
            'left': left + border_left,
            'top': top + border_top,
            'width': client_width,
            'height': client_height
        }
    except Exception as e:
        print(f"[WARNING] Failed to get window rect: {e}")
        return None

def main():
    """Main detection demo function"""
    
    # Load YOLOv12 model
    model_path = Path("runs/train/weights/best.pt")
    
    if not model_path.exists():
        print(f"[ERROR] Model not found: {model_path}")
        print("Please train the model first using start_training.bat")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print(f"[INFO] Loading YOLOv12 model...")
    model = YOLO(str(model_path))
    
    # Force GPU if available
    import torch
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)
    print(f"[INFO] Model loaded successfully on {device.upper()}!")
    
    # Find CS2.exe process
    print("[INFO] Searching for CS2.exe process...")
    cs2_pid = find_cs2_process()
    
    if not cs2_pid:
        print("[ERROR] CS2.exe process not found!")
        print("[INFO] Please start Counter-Strike 2 and try again.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print(f"[INFO] CS2.exe found! (PID: {cs2_pid})")
    
    # Find CS2 window
    print("[INFO] Locating CS2 window...")
    hwnd = find_window_by_pid(cs2_pid)
    
    if not hwnd:
        print("[ERROR] CS2 window not found!")
        print("[INFO] Make sure CS2 is not minimized.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print(f"[INFO] CS2 window found! (Handle: {hwnd})")
    
    # Get window capture region
    capture_region = get_window_rect_for_mss(hwnd)
    
    if not capture_region:
        print("[ERROR] Failed to get CS2 window region!")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    window_width = capture_region['width']
    window_height = capture_region['height']
    print(f"[INFO] CS2 resolution: {window_width}x{window_height}")
    
    # Calculate display size (half of game resolution)
    display_width = window_width // 2
    display_height = window_height // 2
    print(f"[INFO] Display window: {display_width}x{display_height} (50% scale)")
    print("\n[INFO] Starting detection demo...")
    print("[INFO] Controls:")
    print("  - Press 'q' to quit")
    print("  - Press 's' to save screenshot")
    print("  - Press 'c' to toggle class names")
    print("  - Press 'r' to reconnect to CS2 window")
    print("\n")
    
    # Create window with fixed size
    window_name = 'CS2 YOLOv12 Detection Demo'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, display_width, display_height)
    
    # FPS tracking
    fps = 0
    frame_count = 0
    fps_time = time.time()
    show_class_names = True
    screenshot_count = 0
    
    # Performance optimization: use smaller inference size
    inference_size = 640  # Reduced from default for speed
    
    # Color scheme
    colors = {
        'CT': (255, 255, 0),      # Cyan for CT
        'CT_head': (0, 0, 255),   # Red for CT head
        'T': (0, 255, 255),       # Yellow for T
        'T_head': (0, 128, 255),  # Orange for T head
    }
    
    print("[DEMO] Running... (displaying detections)")
    print(f"[INFO] Capturing CS2.exe window (PID: {cs2_pid})")
    print(f"[INFO] Inference size: {inference_size}x{inference_size} for speed")
    
    # MSS instance
    sct = mss.mss()
    
    try:
        while True:
            loop_start = time.time()
            
            # Check if CS2 process still exists
            if not psutil.pid_exists(cs2_pid):
                print("\n[WARNING] CS2 process terminated!")
                break
            
            # Fast CS2 window capture with MSS (full resolution)
            try:
                screenshot = sct.grab(capture_region)
                frame = np.asarray(screenshot, dtype=np.uint8)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                
                # Verify captured size matches expected
                if frame.shape[1] != window_width or frame.shape[0] != window_height:
                    print(f"[WARNING] Captured size mismatch: {frame.shape[1]}x{frame.shape[0]} vs {window_width}x{window_height}")
                    # Update capture region
                    capture_region = get_window_rect_for_mss(hwnd)
                    if capture_region:
                        window_width = capture_region['width']
                        window_height = capture_region['height']
                        display_width = window_width // 2
                        display_height = window_height // 2
                        cv2.resizeWindow(window_name, display_width, display_height)
                    continue
                    
            except Exception as e:
                print(f"[WARNING] Capture failed: {e}")
                print("[INFO] Trying to reconnect to CS2 window...")
                capture_region = get_window_rect_for_mss(hwnd)
                if not capture_region:
                    print("[ERROR] Failed to reconnect!")
                    break
                continue
            
            # OPTIMIZED: Run inference on full frame at reduced size for speed
            # YOLOv12 with imgsz=640, half precision if possible, low conf threshold
            results = model(
                frame, 
                imgsz=inference_size,
                conf=0.4,  # Lower threshold for better recall
                iou=0.5,
                half=True if device == 'cuda' else False,  # FP16 on GPU
                verbose=False,
                device=device
            )
            
            # Process detections and draw on frame
            detection_count = 0
            if len(results) > 0 and results[0].boxes is not None:
                boxes = results[0].boxes
                detection_count = len(boxes)
                
                for box in boxes:
                    # Get box coordinates (already scaled by YOLO)
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    # Get class info
                    conf = float(box.conf[0].cpu().numpy())
                    cls = int(box.cls[0].cpu().numpy())
                    class_name = model.names[cls]
                    
                    # Get color
                    color = colors.get(class_name, (0, 255, 0))
                    
                    # Draw box
                    thickness = 3 if 'head' in class_name.lower() else 2
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
                    
                    # Draw label (optimized)
                    if show_class_names:
                        label = f"{class_name} {conf:.2f}"
                        font_scale = 0.5
                        cv2.putText(frame, label, (x1 + 5, y1 - 5),
                                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2)
                    
                    # Draw center point
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    cv2.circle(frame, (center_x, center_y), 4, color, -1)
            
            # Draw crosshair (simplified)
            center_x = window_width // 2
            center_y = window_height // 2
            cv2.drawMarker(frame, (center_x, center_y), (0, 255, 0),
                          cv2.MARKER_CROSS, 20, 2)
            
            # Draw compact info overlay
            font_scale = 0.6
            cv2.rectangle(frame, (0, 0), (320, 140), (0, 0, 0), -1)
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 25),
                       cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), 2)
            cv2.putText(frame, f"Detections: {detection_count}", (10, 55),
                       cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), 2)
            cv2.putText(frame, f"Resolution: {window_width}x{window_height}", (10, 85),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"Device: {device.upper()}", (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"CS2 PID: {cs2_pid}", (10, 135),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Draw compact legend
            legend_y = window_height - 120
            cv2.rectangle(frame, (0, legend_y), (200, window_height), (0, 0, 0), -1)
            legend_y += 20
            for class_name, color in colors.items():
                cv2.rectangle(frame, (10, legend_y - 10), (25, legend_y), color, -1)
                cv2.putText(frame, class_name, (35, legend_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                legend_y += 25
            
            # Resize frame to display size (50% of game resolution)
            display_frame = cv2.resize(frame, (display_width, display_height), 
                                      interpolation=cv2.INTER_LINEAR)
            
            # Show resized frame
            cv2.imshow(window_name, display_frame)
            
            # FPS calculation
            frame_count += 1
            current_time = time.time()
            if current_time - fps_time >= 1.0:
                fps = frame_count / (current_time - fps_time)
                frame_count = 0
                fps_time = current_time
                print(f"[STATS] FPS: {fps:.1f} | Detections: {detection_count}")
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n[INFO] Quitting demo...")
                break
            elif key == ord('s'):
                screenshot_count += 1
                filename = f"demo_screenshot_{screenshot_count}.jpg"
                # Save full resolution frame, not display frame
                cv2.imwrite(filename, frame)
                print(f"[INFO] Screenshot saved: {filename} ({window_width}x{window_height})")
            elif key == ord('c'):
                show_class_names = not show_class_names
                print(f"[INFO] Class names: {'ON' if show_class_names else 'OFF'}")
            elif key == ord('r'):
                # Reconnect to CS2 window
                print("[INFO] Reconnecting to CS2 window...")
                cs2_pid = find_cs2_process()
                if cs2_pid:
                    hwnd = find_window_by_pid(cs2_pid)
                    if hwnd:
                        capture_region = get_window_rect_for_mss(hwnd)
                        if capture_region:
                            window_width = capture_region['width']
                            window_height = capture_region['height']
                            display_width = window_width // 2
                            display_height = window_height // 2
                            cv2.resizeWindow(window_name, display_width, display_height)
                            print(f"[INFO] Reconnected! Game: {window_width}x{window_height}, Display: {display_width}x{display_height}")
                        else:
                            print("[WARNING] Failed to get window region")
                    else:
                        print("[WARNING] Window not found")
                else:
                    print("[WARNING] CS2 process not found")
            
            # No sleep - maximize FPS
            
            # FPS calculation
            frame_count += 1
            current_time = time.time()
            if current_time - fps_time >= 1.0:
                fps = frame_count / (current_time - fps_time)
                frame_count = 0
                fps_time = current_time
                print(f"[STATS] FPS: {fps:.1f} | Detections: {detection_count}")
    
    finally:
        sct.close()
        cv2.destroyAllWindows()
    print("\n[INFO] Demo finished!")
    print(f"[STATS] Final FPS: {fps:.1f}")
    print(f"[STATS] Screenshots saved: {screenshot_count}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Demo interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
