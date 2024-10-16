import torch
import cv2
import os
from PIL import ImageFile


# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or 'yolov5m', 'yolov5l', 'yolov5x'

# Directory containing the images
image_dir = r'C:\Users\Admin.DESKTOP-M4R2VLU\week7\images'  
results_dir = r'C:\Users\Admin.DESKTOP-M4R2VLU\week7\Results'  

if not os.path.exists(results_dir):
    os.makedirs(results_dir)
ImageFile.LOAD_TRUNCATED_IMAGES = True
# Process each image in the directory
for image_name in os.listdir(image_dir):
    if image_name.endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(image_dir, image_name)
        
        # Perform detection
        results = model(img_path)
        
        # Save or display results
        results.save(save_dir=results_dir)  # Save detection results
        results.show()  # Display results

        # Access detection results
for result in results.xyxy[0]:  # Get the detections for the first image
    x1, y1, x2, y2, conf, cls = result  # Unpack the results
    print(f'Bounding Box: ({x1}, {y1}), ({x2}, {y2}) - Confidence: {conf:.2f}, Class: {cls}')