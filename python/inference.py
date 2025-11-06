"""
YOLOv12 Inference Script
Run inference on images or video with trained model
"""
import sys
import cv2
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
        print("   Please train a model first: python train.py")
        return None
    
    # Find all training runs
    train_dirs = sorted(runs_dir.glob("train*"))
    if not train_dirs:
        print("❌ No trained model found!")
        return None
    
    # Get latest run
    latest_run = train_dirs[-1]
    
    # Check for best.pt
    best_weights = latest_run / "weights" / "best.pt"
    if best_weights.exists():
        return str(best_weights)
    
    print("❌ No best.pt found in training results!")
    return None

def run_inference_image(model, image_path, output_path=None):
    """Run inference on a single image"""
    print(f"📸 Processing: {image_path}")
    
    # Read image
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"❌ Could not read image: {image_path}")
        return
    
    # Run inference
    results = model(image, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    
    # Annotate image
    box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    
    annotated_image = box_annotator.annotate(scene=image.copy(), detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)
    
    # Save or display
    if output_path:
        cv2.imwrite(str(output_path), annotated_image)
        print(f"✅ Saved to: {output_path}")
    else:
        # Display
        cv2.imshow("YOLOv12 Inference", annotated_image)
        print("Press any key to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    # Print detections
    print(f"   Detected {len(detections)} objects")
    for i, (bbox, class_id, confidence) in enumerate(zip(detections.xyxy, detections.class_id, detections.confidence)):
        print(f"   {i+1}. Class {class_id}: {confidence:.2%}")

def run_inference_video(model, video_path, output_path=None):
    """Run inference on video"""
    print(f"🎥 Processing video: {video_path}")
    
    # Open video
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"❌ Could not open video: {video_path}")
        return
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps}")
    print(f"   Total Frames: {total_frames}")
    
    # Setup output video
    writer = None
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    # Annotators
    box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Run inference
            results = model(frame, verbose=False)[0]
            detections = sv.Detections.from_ultralytics(results)
            
            # Annotate
            annotated_frame = box_annotator.annotate(scene=frame.copy(), detections=detections)
            annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections)
            
            # Write or display
            if writer:
                writer.write(annotated_frame)
                print(f"\r   Processing: {frame_count}/{total_frames} frames ({frame_count/total_frames*100:.1f}%)", end="")
            else:
                cv2.imshow("YOLOv12 Inference", annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\n   Stopped by user")
                    break
        
        print()
        
    finally:
        cap.release()
        if writer:
            writer.release()
            print(f"✅ Saved to: {output_path}")
        cv2.destroyAllWindows()

def main():
    """Main inference function"""
    print("=" * 70)
    print("YOLOv12 Inference")
    print("=" * 70)
    print()
    
    # Find best model
    weights_path = find_best_weights()
    if not weights_path:
        return
    
    print(f"🤖 Loading model: {weights_path}")
    model = YOLO(weights_path)
    print("✅ Model loaded successfully!")
    print()
    
    # Get input
    print("📁 Input Options:")
    print("   1. Image file (jpg, png, etc.)")
    print("   2. Video file (mp4, avi, etc.)")
    print("   3. Webcam (0)")
    print()
    
    input_path = input("Enter path or option (0 for webcam): ").strip()
    print()
    
    # Check if webcam
    if input_path == "0":
        print("📹 Starting webcam inference...")
        print("   Press 'q' to quit")
        print()
        run_inference_video(model, 0)
        return
    
    input_path = Path(input_path)
    
    # Check if exists
    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        return
    
    # Check if image or video
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    
    if input_path.suffix.lower() in image_extensions:
        # Ask for output
        save = input("Save annotated image? (y/n): ").lower() == 'y'
        output_path = None
        if save:
            output_path = input_path.parent / f"{input_path.stem}_annotated{input_path.suffix}"
        
        print()
        run_inference_image(model, input_path, output_path)
        
    elif input_path.suffix.lower() in video_extensions:
        # Ask for output
        save = input("Save annotated video? (y/n): ").lower() == 'y'
        output_path = None
        if save:
            output_path = input_path.parent / f"{input_path.stem}_annotated.mp4"
        
        print()
        run_inference_video(model, input_path, output_path)
        
    else:
        print(f"❌ Unsupported file format: {input_path.suffix}")
        print(f"   Supported: {', '.join(image_extensions + video_extensions)}")

if __name__ == "__main__":
    main()
