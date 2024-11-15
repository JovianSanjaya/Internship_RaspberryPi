input_dir = f"./values/subtracted/subtracted_rgb_0_2.txt"

with open(input_dir,"r") as file:
    lines = file.readlines()
    print(len(lines)) #54*23 = 1242