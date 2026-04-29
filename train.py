import numpy as np
from ultralytics import YOLO

# model = YOLO("../runs/detect/train/weights/best.pt")

# model = YOLO("yolov8n.pt")

# model.train(data="../data.yaml",epochs=1000,task='detect',batch=16,imgsz=640,device=0,workers=8) (GPU)

# model.train(data="../data.yaml",epochs=1000,task='detect',batch=16,imgsz=640,device='cpu',workers=8) (CPU)

# model.train(data="data.yaml",epochs=100)