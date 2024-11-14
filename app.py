import cv2
import time
import requests
from ultralytics import YOLO
from picamera2 import Picamera2
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Initialize Flask app and SocketIO with CORS support
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow connections from any origin

# Define model path and load model
weight_path = "./models/best_ncnn_model"
model = YOLO(weight_path)

# Defect categories and their colors
colors = {
    'Nicks': {'color': (60, 60, 255), 'thickness': 2},
    'Dents': {'color': (148, 156, 255), 'thickness': 2},
    'Scratches': {'color': (28, 116, 255), 'thickness': 2},
    'Pittings': {'color': (28, 180, 255), 'thickness': 2}
}

picam2 = Picamera2()
picam2.start()

time.sleep(2)

# Dictionary to keep track of detected defects count
defect_counts = {'Nicks': 0, 'Dents': 0, 'Scratches': 0, 'Pittings': 0}

# ThingSpeak Channel details
CHANNEL_ID = '2738238'  # Replace with your ThingSpeak channel ID
WRITE_API_KEY = '20MGE1MRG7BQ9PHS'  # Replace with your Write API key
THING_SPEAK_URL = f'https://api.thingspeak.com/update?api_key={WRITE_API_KEY}'

# Flask route for the homepage
@app.route('/')
def index():
    return render_template('index.html')  # HTML file that contains your Chart.js chart

# Function to update ThingSpeak
def update_thingspeak():
    params = {
        'api_key': WRITE_API_KEY,
        'field1': defect_counts['Nicks'],
        'field2': defect_counts['Dents'],
        'field3': defect_counts['Scratches'],
        'field4': defect_counts['Pittings']
    }
    try:
        response = requests.get(THING_SPEAK_URL, params=params)
        if response.status_code == 200:
            print("Successfully updated ThingSpeak.")
        else:
            print(f"Failed to update ThingSpeak. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error updating ThingSpeak: {e}")

# Process frames from the camera
def process_frame():
    last_update_time = time.time()  # To track the frequency of ThingSpeak updates
    while True:
        frame = picam2.capture_array()
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Run detection
        results = model(image)
        detections = results[0].boxes

        # Reset counts for each frame
        local_defect_counts = {'Nicks': 0, 'Dents': 0, 'Scratches': 0, 'Pittings': 0}

        # Process detections
        for box in detections:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            confidence = box.conf[0].cpu().numpy()
            class_id = int(box.cls[0].cpu().numpy())
            class_name = model.names[class_id]

            if class_name in colors:
                local_defect_counts[class_name] += 1

            # Draw bounding boxes on the image with colors
            color = colors[class_name]['color']
            thickness = colors[class_name]['thickness']
            label = f"{class_name}: {confidence:.2f}"
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
            cv2.putText(image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

        # Update global defect counts
        for key in defect_counts:
            defect_counts[key] = local_defect_counts[key]

        # Send defect counts to frontend via SocketIO
        socketio.emit('update_counts', defect_counts)

        # Show the image in real time
        cv2.imshow("OIS Real-Time AI Defect Detection", image)

       #update thingspeak
        update_thingspeak()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Start a background thread for processing frames
@socketio.on('connect')
def handle_connect():
    print("Client connected.")
    socketio.start_background_task(target=process_frame)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)