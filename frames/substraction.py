#changed
n1=1
#fixed
n2=2

first_frame_dir = f"./values/original/frame_{n1}_rgb_matrices.txt"
second_frame_dir = f"./values/original/frame_{n2}_rgb_matrices.txt"
output_dir = f"./values/subtracted/subtracted_rgb_{n1}_{n2}.txt"

# Function to read RGB values from a file, with more robust parsing
def read_rgb_values(file_path):
    with open(file_path, 'r') as file:
        content = file.read().replace('\n', ' ').strip()  # Replace newlines with spaces and trim
        # Split the content by ') (' to get individual RGB groups
        raw_rgb_values = content.split(') (')
        rgb_values = []
        for item in raw_rgb_values:
            # Clean up the item and split it into RGB components
            clean_item = item.strip('() ')
            try:
                r, g, b = map(int, clean_item.split(','))
                rgb_values.append((r, g, b))
            except ValueError:
                print(f"Skipping invalid entry: {clean_item}")
    return rgb_values

# Read RGB values from both files
first_frame_rgb = read_rgb_values(first_frame_dir)
second_frame_rgb = read_rgb_values(second_frame_dir)

# Subtract RGB values and clamp negatives to 0
result_rgb = []
min_length = min(len(first_frame_rgb), len(second_frame_rgb))

for i in range(min_length):
    r0, g0, b0 = first_frame_rgb[i]
    r1, g1, b1 = second_frame_rgb[i]
    result_rgb.append((max(r0 - r1, 0), max(g0 - g1, 0), max(b0 - b1, 0)))

# Save the result to the output file
with open(output_dir, 'w') as file:
    for rgb in result_rgb:
        file.write(f"{rgb}\n")

print(f"Result saved to {output_dir}")