import cv2
import numpy as np

def save_rgb_matrices_to_txt(image_path, output_txt_path):
    # Load the image
    image = cv2.imread(image_path)

    # Check if the image was loaded correctly
    if image is None:
        print(f"Error: Could not open or find the image at {image_path}")
        return

    # Convert the image from BGR (OpenCV default) to RGB format
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Get the image dimensions
    height, width, channels = image_rgb.shape
    print(f"Image Dimensions: {width}x{height} pixels")

    # Open a text file to write the RGB values
    with open(output_txt_path, 'w') as file:
        file.write(f"Image Dimensions: {width}x{height} pixels\n")
        file.write("RGB Matrices:\n")

        # Iterate over each pixel and write the RGB values to the file
        for y in range(height):
            row = []
            for x in range(width):
                # Get the RGB values of the pixel at (x, y)
                r, g, b = image_rgb[y, x]
                # Format as (R, G, B) and add to the row
                row.append(f"({r},{g},{b})")
            # Join the row values and write them to the file
            file.write(' '.join(row) + '\n')

    print(f"RGB values saved to {output_txt_path}")

# Example usage
image_path = './frames/frame_3.jpg'  # Replace with the path to your .jpg file
output_txt_path = 'frame_3_rgb_matrices.txt'  # Output .txt file path

save_rgb_matrices_to_txt(image_path, output_txt_path)
