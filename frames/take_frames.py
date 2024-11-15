import cv2
from ultralytics import YOLO
import numpy as np
from picamera2 import Picamera2
import time
import os

# Set up the directory to save frames
save_directory = "/home/pi/Internship/frames"
os.makedirs(save_directory, exist_ok=True)

# Define the weight path
weight_path = "./models/personal model/best_ncnn_model"

# Load the model
model = YOLO(weight_path)

# Define colors for bounding boxes
colors = {
    'Nicks': {'color': (60, 60, 255), 'thickness': 2},     # Nicks (Red) in BGR
    'Dents': {'color': (148, 156, 255), 'thickness': 2},   # Dents (Light Red) in BGR
    'Scratches': {'color': (28, 116, 255), 'thickness': 2}, # Scratches (Orange) in BGR
    'Pittings': {'color': (28, 180, 255), 'thickness': 2}   # Pittings (Yellow) in BGR
}

# Initialize the camera
picam2 = Picamera2()
picam2.start()

# Wait for the camera to adjust
time.sleep(2)

frame_count = 0  # Frame counter for saved images

try:
    while True:
        # Capture the frame from the camera
        frame = picam2.capture_array()
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Perform detection on the image
        results = model(image)
        detections = results[0].boxes

        # Draw bounding boxes and labels
        for box in detections:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()  # Bounding box coordinates
            confidence = box.conf[0].cpu().numpy()      # Confidence score
            class_id = int(box.cls[0].cpu().numpy())    # Class ID

            # Get the class name
            class_name = model.names[class_id]

            # Determine the color and thickness for the bounding box
            if class_name in colors:
                color = colors[class_name]['color']
                thickness = colors[class_name]['thickness']
            else:
                color = (255, 0, 0)  # Default color if class is unknown
                thickness = 2

            # Label with class name and confidence score
            label = f"{class_name}: {confidence:.2f}"
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
            cv2.putText(image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

        # Display the image with bounding boxes
        cv2.imshow("OIS Real Time AI Defect Detection", image)

        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Save the current frame
            frame_path = os.path.join(save_directory, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, image)
            print(f"Frame saved to: {frame_path}")
            frame_count += 1

finally:
    # Stop the camera and close windows
    picam2.stop()
    cv2.destroyAllWindows()
