# 🎯 CS2 YOLOv12 Detection Project

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![YOLOv12](https://img.shields.io/badge/YOLOv12-Ultralytics-00FFFF.svg)](https://github.com/ultralytics/ultralytics)
[![License](https://img.shields.io/badge/License-Educational-green.svg)](LICENSE)

An educational project demonstrating real-time object detection using YOLOv12 on Counter-Strike 2. This project showcases computer vision techniques, deep learning model training, and real-time inference.

## 🎬 Demo Video

https://github.com/user-attachments/assets/ecb1bdc1-37f6-4912-b292-332098fac91f

*Real-time detection running at 24+ FPS with YOLOv12 - Detecting CT, CT_head, T, and T_head classes*

**[📥 Download Demo Video](https://github.com/user-attachments/assets/ecb1bdc1-37f6-4912-b292-332098fac91f)**

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Demo](#demo)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Training](#training)
- [Performance](#performance)
- [Technologies Used](#technologies-used)
- [Educational Purpose](#educational-purpose)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project implements a custom-trained YOLOv12 object detection model to identify and classify players in Counter-Strike 2. The system can detect:

- **CT (Counter-Terrorist)** - Body detection
- **CT_head** - Head detection for Counter-Terrorists
- **T (Terrorist)** - Body detection
- **T_head** - Head detection for Terrorists

The project demonstrates end-to-end machine learning workflow including data collection, model training, optimization, and real-time inference.

## ✨ Features

- 🚀 **Real-time Detection**: High-performance inference with 60+ FPS
- 🎯 **Multi-class Detection**: Separate detection for heads and bodies
- 🎮 **Game Integration**: Optimized for Counter-Strike 2 visual recognition
- 📊 **Training Pipeline**: Complete training workflow with YOLOv12
- 🖼️ **Live Visualization**: OpenCV-based real-time display
- ⚡ **GPU Acceleration**: CUDA support for NVIDIA GPUs
- 📈 **Performance Monitoring**: FPS tracking and detection statistics

## 🎬 Demo

**⚠️ IMPORTANTE: O CS2 deve estar em execução antes de rodar o demo!**

Run the real-time detection demo:

```bash
demo_yolo.bat
```

The demo **automatically detects the CS2.exe process** and captures only the game window for maximum performance.

**Features:**
- 🎮 **CS2.exe Process Detection**: Automatically finds and captures only the CS2 game window
- 🖥️ **Full Window Capture**: Captures entire CS2 window at native resolution
- ⚡ **Optimized Performance**: 24+ FPS guaranteed with smart inference scaling
- 📊 **Real-time Stats**: FPS counter, detection count, and process monitoring
- 🎯 **GPU Acceleration**: Automatic CUDA detection and FP16 inference

**Demo Controls:**
- `q` - Quit demo
- `s` - Save screenshot
- `c` - Toggle class name display
- `r` - Reconnect to CS2 window (if changed/minimized)

## 📊 Dataset

The model is trained on a custom CS2 dataset with 4 classes:

| Class | Description | Count |
|-------|-------------|-------|
| CT | Counter-Terrorist body | ~1000 images |
| CT_head | Counter-Terrorist head | ~1000 images |
| T | Terrorist body | ~1000 images |
| T_head | Terrorist head | ~1000 images |

Dataset format: YOLO v8/v12 compatible annotations

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- NVIDIA GPU with CUDA support (recommended)
- 6GB+ VRAM for training
- Windows 10/11 (tested on Windows)

**Important:** This project requires `opencv-contrib-python` for Windows GUI support. The standard `opencv-python` may not work correctly on Windows.

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/cs2-yolov12-detection.git
cd cs2-yolov12-detection
```

2. **Quick Setup (Recommended for Windows):**
```bash
setup_demo.bat
```

This will create a virtual environment and install all dependencies automatically.

Or manual setup:

3. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

**Note:** If you encounter OpenCV GUI errors on Windows, ensure you have `opencv-contrib-python` installed:
```bash
pip uninstall opencv-python opencv-python-headless -y
pip install opencv-contrib-python==4.10.0.84
```

4. **Download pre-trained weights (optional):**
- Place `best.pt` in `runs/train/weights/`

## 🚀 Usage

### Quick Start - Demo

Run the detection demo to see the model in action:

```bash
demo_yolo.bat
```

This will:
1. Load the trained YOLOv12 model
2. Capture the center region of your screen
3. Display real-time detections with bounding boxes
4. Show FPS and detection statistics

### Training Your Own Model

1. **Prepare dataset:**
   - Place images in `datasets/cs2-1/train/images`
   - Place labels in `datasets/cs2-1/train/labels`
   - Update `datasets/cs2-1/data.yaml`

2. **Configure training:**
   - Edit `config.yaml` for hyperparameters
   - Adjust batch size based on your GPU

3. **Start training:**
```bash
start_training.bat
```

4. **Monitor progress:**
   - Training logs in `runs/train/`
   - TensorBoard: `tensorboard --logdir=runs`

### Python API

```python
from ultralytics import YOLO

# Load trained model
model = YOLO('runs/train/weights/best.pt')

# Run inference
results = model('image.jpg', conf=0.5)

# Process results
for result in results:
    boxes = result.boxes
    for box in boxes:
        print(f"Class: {model.names[int(box.cls)]}")
        print(f"Confidence: {box.conf:.2f}")
```

## 📁 Project Structure

```
cs2-yolov12-detection/
├── datasets/              # Training datasets
│   └── cs2-1/
│       ├── train/         # Training images & labels
│       ├── valid/         # Validation set
│       └── test/          # Test set
├── runs/                  # Training outputs
│   └── train/
│       └── weights/       # Model checkpoints
├── yolov12/              # YOLOv12 framework
├── python/               # Python utilities
│   ├── train.py          # Training script
│   ├── inference.py      # Inference utilities
│   └── validate.py       # Validation script
├── demo_detection.py     # Real-time demo script
├── demo_yolo.bat         # Demo launcher
├── config.yaml           # Training configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🎓 Training

### Configuration

Edit `config.yaml` to customize training:

```yaml
model:
  checkpoint: "yolov12n.pt"  # or yolov12s, yolov12m, etc.

training:
  epochs: 300
  batch_size: 8
  imgsz: 640
  device: 0
  
  # Optimizer
  optimizer: "AdamW"
  lr0: 0.001
  
  # Augmentation
  hsv_h: 0.015
  hsv_s: 0.7
  flipud: 0.0
  fliplr: 0.5
```

### Training Process

1. **Data Loading**: Automatic dataset loading from `data.yaml`
2. **Augmentation**: HSV, flip, scale, translate augmentations
3. **Training**: AdamW optimizer with learning rate scheduling
4. **Validation**: Automatic validation every epoch
5. **Checkpointing**: Save best and last models

### Monitoring

```bash
# TensorBoard
tensorboard --logdir=runs/train

# Or check results.csv
runs/train/results.csv
```

## 📈 Performance

### Detection Performance

- **FPS**: 60-120 FPS (RTX 3060+)
- **Accuracy**: mAP@0.5: ~0.85
- **Inference Time**: ~8-15ms per frame
- **Model Size**: ~6MB (YOLOv12n)

### Optimization Tips

1. **Use smaller model**: YOLOv12n for speed, YOLOv12l for accuracy
2. **Reduce input size**: 640x640 → 416x416 for 2x speed
3. **Enable TensorRT**: For NVIDIA GPUs
4. **Use FP16**: Half-precision inference

## 🛠️ Technologies Used

- **Deep Learning Framework**: [Ultralytics YOLOv12](https://github.com/ultralytics/ultralytics)
- **Computer Vision**: OpenCV
- **Deep Learning**: PyTorch
- **GPU Acceleration**: CUDA
- **Screen Capture**: MSS (Multiple Screen Shots)
- **Data Annotation**: Roboflow

## 📚 Educational Purpose

This project is designed for educational purposes to demonstrate:

### Computer Vision Concepts
- Object detection architectures (YOLO)
- Real-time image processing
- Bounding box prediction
- Non-maximum suppression

### Machine Learning Workflow
- Dataset preparation and annotation
- Model training and hyperparameter tuning
- Validation and testing strategies
- Model optimization techniques

### Software Engineering
- Python project structure
- GPU acceleration
- Real-time performance optimization
- Cross-platform compatibility

### Practical Applications
- Real-time object detection
- Multi-class classification
- Screen capture and processing
- Visual feedback systems

## ⚠️ Disclaimer

**This project is for educational and research purposes only.**

- Demonstrates computer vision and deep learning techniques
- Should not be used in online multiplayer games
- Intended for offline testing and learning
- Respects game terms of service when used appropriately

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Areas for Contribution

- [ ] Additional dataset examples
- [ ] Model optimization techniques
- [ ] Performance benchmarks
- [ ] Documentation improvements
- [ ] Cross-platform support (Linux, macOS)
- [ ] Additional visualization features

## 📝 Development Roadmap

- [x] Basic YOLOv12 training pipeline
- [x] Real-time detection demo
- [x] Multi-class detection (CT/T, head/body)
- [ ] TensorRT optimization
- [ ] ONNX export support
- [ ] Web-based demo interface
- [ ] Mobile deployment (iOS/Android)
- [ ] Advanced augmentation techniques

## 📖 Documentation

For more detailed documentation:

- [Training Guide](docs/TRAINING.md) - Detailed training instructions
- [API Reference](docs/API.md) - Python API documentation
- [Performance Tuning](docs/PERFORMANCE.md) - Optimization guide

## 🙏 Acknowledgments

- [Ultralytics](https://github.com/ultralytics/ultralytics) for YOLOv12
- [Roboflow](https://roboflow.com/) for dataset management
- Counter-Strike 2 community

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

- **LinkedIn**: [Your LinkedIn Profile](https://linkedin.com/in/yourprofile)
- **GitHub**: [@yourusername](https://github.com/yourusername)
- **Email**: your.email@example.com

---

⭐ If you find this project useful, please consider giving it a star!

**Made with ❤️ for the Computer Vision community**
