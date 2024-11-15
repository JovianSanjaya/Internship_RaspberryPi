import numpy as np
import os
import plotly.graph_objects as go

n1 = 1
n2 = 2

# Step 1: Read the values from the text file
filename = f"./values/subtracted/subtracted_rgb_{n1}_{n2}.txt"
rgb_values = []

with open(filename, "r") as file:
    for line in file:
        # Strip any whitespace and split by commas
        line = line.strip().strip('()')
        rgb = tuple(map(int, line.split(',')))
        rgb_values.append(rgb)

# Step 2: Calculate the average of each pixel's RGB values
averaged_rgb_values = []
for rgb in rgb_values:
    avg_rgb = sum(rgb) / 3  # Average of R, G, B
    averaged_rgb_values.append(avg_rgb)

# Convert to a numpy array for easier handling
averaged_rgb_values = np.array(averaged_rgb_values)



# Step 6: Save the averaged RGB values to a new text file
average_output_directory = "./values/average_rgb"  # Specify the directory to save the average values
os.makedirs(average_output_directory, exist_ok=True)  # Create the directory if it doesn't exist

average_filename = os.path.join(average_output_directory, f"averaged_rgb_{n1}_{n2}.txt")

# Write the averaged RGB values to the text file
with open(average_filename, "w") as f:
    for avg in averaged_rgb_values:
        f.write(f"{avg}\n")  # Write each averaged value in a new line

print(f"Averaged RGB values saved to {average_filename}")









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
output_directory = "./heatmap/"  # Specify the desired output directory
os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
output_filename = os.path.join(output_directory, f"interactive_heatmap_{n1}_{n2}.html")

# Save the figure as an HTML file
fig.write_html(output_filename)

# Optionally, display the heatmap in the browser
fig.show()

print(f"Interactive heatmap saved to {output_filename}")
