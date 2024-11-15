import cv2
from picamera2 import Picamera2
import numpy as np

# Initialize Picamera2
picam2 = Picamera2()

# Configure the camera (setting resolution and format)
picam2.configure(picam2.create_still_configuration())

# Start the camera stream
picam2.start()

# Create an OpenCV window to display the video stream
cv2.namedWindow("Camera Stream", cv2.WINDOW_NORMAL)

try:
    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()

        # Convert the frame from RGB to BGR for OpenCV compatibility
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Display the frame in the OpenCV window
        cv2.imshow("Camera Stream", frame_bgr)

        # Check for user input to exit (press 'q' to quit)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop the camera stream and close the window
    picam2.stop()
    cv2.destroyAllWindows()
