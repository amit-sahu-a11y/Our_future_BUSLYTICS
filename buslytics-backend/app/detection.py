from ultralytics import YOLO
import cv2
import numpy as np

# Load model once
model = YOLO("yolov8n.pt")  # lightweight & fast

def detect_person_count(image_bytes: bytes) -> int:
    # Convert bytes → OpenCV image
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Run detection
    results = model(img, conf=0.5, classes=[0])  # class 0 = person

    # Count persons
    count = len(results[0].boxes)
    return count
