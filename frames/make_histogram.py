import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

n=3

# File path for the input text file and output directory
input_file_path = f'./values/original/frame_{n}_rgb_matrices.txt'
output_dir = './histogram/'  # Change to your desired directory

# Read the file and extract numbers
red_values = []
green_values = []
blue_values = []

with open(input_file_path, 'r') as file:
    for line in file:
        # Split the line into individual tuples, and remove any unnecessary whitespace
        line = line.strip()
        
        # Split the line by space to get the individual tuples
        tuples = line.split(' ')  # Space is the delimiter
        
        # Process each tuple (strip the parentheses and split by commas)
        for tup in tuples:
            # Clean the tuple and split by commas to get individual values
            cleaned_tup = tup.strip('()').split(',')
            
            # Append the individual RGB values to respective lists
            red_values.append(int(cleaned_tup[0]))
            green_values.append(int(cleaned_tup[1]))
            blue_values.append(int(cleaned_tup[2]))

# Convert the lists into NumPy arrays
red_values = np.array(red_values)
green_values = np.array(green_values)
blue_values = np.array(blue_values)

# Create a subplot figure with 3 rows and 1 column (or adjust layout as needed)
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                    subplot_titles=('Red Channel Histogram', 'Green Channel Histogram', 'Blue Channel Histogram'))

# Add histograms for each RGB channel to the respective subplot
fig.add_trace(go.Histogram(x=red_values, nbinsx=256, name='Red Channel', marker_color='red'),
              row=1, col=1)

fig.add_trace(go.Histogram(x=green_values, nbinsx=256, name='Green Channel', marker_color='green'),
              row=2, col=1)

fig.add_trace(go.Histogram(x=blue_values, nbinsx=256, name='Blue Channel', marker_color='blue'),
              row=3, col=1)

# Update layout for the subplots and axis labels
fig.update_layout(
    title='RGB Channel Histograms',
    xaxis_title='Pixel Value',
    yaxis_title='Frequency',
    template='plotly_dark',  # Use a dark template for better contrast (optional)
    height=900,  # Adjust height for better spacing between histograms
    showlegend=False  # Hide the legend (optional, as each plot is already labeled)
)

# Save the combined histogram plot as an HTML file
output_file_path = f'{output_dir}/combined_rgb_histogram_frame_{n}.html'
fig.write_html(output_file_path)

print(f"Combined RGB histogram saved to {output_file_path}")
