import numpy as np
import os
import plotly.graph_objects as go

n1 = 2

# Step 1: Read the values from the text file
filename = f"./values/original/frame_{n1}_rgb_matrices.txt"
rgb_values = []

with open(filename, 'r') as file:
    content = file.read().replace('\n', ' ').strip()  # Replace newlines with spaces and trim
    # Split the content by ') (' to get individual RGB groups
    raw_rgb_values = content.split(') (')
    for item in raw_rgb_values:
        # Clean up the item and split it into RGB components
        clean_item = item.strip('() ')
        try:
            r, g, b = map(int, clean_item.split(','))
            rgb_values.append((r, g, b))
        except ValueError:
            continue  # Skip any malformed data

# Step 2: Calculate the average of each pixel's RGB values
averaged_rgb_values = []
for rgb in rgb_values:
    avg_rgb = sum(rgb) / 3  # Average of R, G, B
    averaged_rgb_values.append(avg_rgb)

# Convert to a numpy array for easier handling
averaged_rgb_values = np.array(averaged_rgb_values)


# Step 3: Generate the heatmap
# Reshape the values into a 2D array for the heatmap (assuming a grid shape, for example 23x54)
# Adjust the shape to fit your data
height = 23
width = 54

heatmap_data = averaged_rgb_values.reshape((height, width))

# Step 4: Create an interactive heatmap using Plotly
fig = go.Figure(data=go.Heatmap(
    z=heatmap_data,
    colorscale='Hot'  # You can change the color scale (e.g., 'Hot', 'Viridis', 'Jet', etc.)
))

fig.update_layout(
    title="Interactive Heatmap of Averaged RGB Values",
    xaxis_title="X Axis",
    yaxis_title="Y Axis"
)

# Step 5: Save the heatmap to an HTML file
output_directory = "./heatmap/original"  # Specify the desired output directory
os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
output_filename = os.path.join(output_directory, f"interactive_heatmap_frame_{n1}.html")

# Save the figure as an HTML file
fig.write_html(output_filename)

# Optionally, display the heatmap in the browser
fig.show()

print(f"Interactive heatmap saved to {output_filename}")
