from collections import defaultdict

import cv2
import numpy as np

from ultralytics import YOLO

from config import CAR_MODEL_PATH, PLATE_MODEL_PATH

# Load the YOLOv8 model
model = YOLO(PLATE_MODEL_PATH)

# Open the video file
video_path = "new_sample.mp4"

results = model.track(video_path, save=True)