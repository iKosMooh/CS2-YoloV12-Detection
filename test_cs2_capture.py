"""
Test CS2 Window Capture
Quick test to verify CS2 window detection and capture
"""

import cv2
import numpy as np
import win32gui
import win32ui
import win32con
from ctypes import windll
import time

def find_cs2_window():
    """Find CS2 window handle"""
    hwnd = win32gui.FindWindow(None, "Counter-Strike 2")
    if not hwnd:
        hwnd = win32gui.FindWindow(None, "CS2")
    return hwnd

def capture_cs2_window(hwnd):
    """Capture CS2 window"""
    try:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)
        
        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
        
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        img = np.frombuffer(bmpstr, dtype=np.uint8)
        img.shape = (height, width, 4)
        
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)
        
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img, width, height
    except Exception as e:
        print(f"Error: {e}")
        return None, 0, 0

def main():
    print("=" * 50)
    print("CS2 Window Capture Test")
    print("=" * 50)
    print()
    
    print("[1] Searching for CS2 window...")
    hwnd = find_cs2_window()
    
    if not hwnd:
        print("[X] CS2 window not found!")
        print()
        print("Possible window titles:")
        
        def enum_windows_callback(hwnd, results):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title and len(title) > 0:
                    results.append(title)
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        cs2_related = [w for w in windows if 'counter' in w.lower() or 'cs2' in w.lower() or 'cs' in w.lower()]
        if cs2_related:
            print("Found CS2-related windows:")
            for w in cs2_related[:10]:
                print(f"  - {w}")
        else:
            print("No CS2-related windows found")
            print("\nAll windows (first 20):")
            for w in windows[:20]:
                print(f"  - {w}")
        
        input("\nPress Enter to exit...")
        return
    
    print(f"[✓] CS2 window found! (Handle: {hwnd})")
    
    print("[2] Testing window capture...")
    frame, width, height = capture_cs2_window(hwnd)
    
    if frame is None:
        print("[X] Failed to capture window!")
        input("\nPress Enter to exit...")
        return
    
    print(f"[✓] Capture successful!")
    print(f"    Resolution: {width}x{height}")
    print()
    print("[3] Starting live preview...")
    print("    Press 'q' to quit")
    print()
    
    cv2.namedWindow('CS2 Capture Test', cv2.WINDOW_NORMAL)
    
    fps = 0
    frame_count = 0
    fps_time = time.time()
    
    while True:
        loop_start = time.time()
        
        frame, width, height = capture_cs2_window(hwnd)
        
        if frame is None:
            print("[X] Capture failed!")
            break
        
        # Add FPS overlay
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Resolution: {width}x{height}", (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('CS2 Capture Test', frame)
        
        # Calculate FPS
        frame_count += 1
        current_time = time.time()
        if current_time - fps_time >= 1.0:
            fps = frame_count / (current_time - fps_time)
            frame_count = 0
            fps_time = current_time
            print(f"FPS: {fps:.1f} | Resolution: {width}x{height}")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # Target 60 FPS
        loop_time = time.time() - loop_start
        if loop_time < 1.0/60.0:
            time.sleep(1.0/60.0 - loop_time)
    
    cv2.destroyAllWindows()
    print("\n[✓] Test complete!")
    print(f"    Final FPS: {fps:.1f}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
