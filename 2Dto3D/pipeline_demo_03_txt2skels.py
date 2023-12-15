import os
from ast import Delete
from dataclasses import replace
import os
import tempfile
import shutil
import time
import math

mode = "dev"

# Read the dev.files file for a list of folder names
with open(f"input_data/{mode}.files", "r") as file:
    folder_names = file.read().splitlines()

# Walk through each folder
for folder_name in folder_names:
    
    if mode == "dev":
        folder_name_without_head= folder_name[4:] # Remove the train/ dev/ test/ at the beginning of each line
    elif mode == "test":
        folder_name_without_head= folder_name[5:] # Remove the train/ dev/ test/ at the beginning of each line
    elif mode == "train":
        folder_name_without_head= folder_name[6:] # Remove the train/ dev/ test/ at the beginning of each line

    folder_path = os.path.join(f"out_data/{mode}", folder_name_without_head)
    demo5_path = os.path.join(folder_path, "demo5.txt")
    
    # Check whether the demo5.txt file exists
    if os.path.exists(demo5_path):
        output = ""
        with open(demo5_path, "r") as demo5_file:
            lines = demo5_file.read().splitlines()
            line_count = len(lines)
            
            # Walk through each line of demo5.txt
            for i, line in enumerate(lines, 1):
                numbers = line.split()
                
                # Process each number: divide by 9 and add the number of times
                vid_time = round(i / line_count, 5)  # Keep 5 decimal places
                #processed_numbers = [format(float(num) / 9, ".5f") for num in numbers]  # 保留5位小数
                processed_numbers = [format(float(num) / 9, ".5f") if num is not None and not math.isnan(float(num)) and float(num) != 0.00000 and float(num) != -0.00000 else "0.01600" for num in numbers]
                
                output += " ".join(processed_numbers)
                
                # Separate lines with Spaces
                if i <= line_count:
                    output += f" {vid_time} "
        
        # Write the processing results to the dev.skels file
        with open(f"final_data/{mode}.skels", "a") as skels_file:
            skels_file.write(output + "\n")

        with open(f"final_data/{mode}_exist_demo5_folder.txt", "a") as exist_file:
            exist_file.write(folder_name_without_head + "\n")

    else:
        # If demo5.txt does not exist in the folder, save the folder name to missing.txt
        with open(f"final_data/{mode}_missing_demo5_folder.txt", "a") as missing_file:
            missing_file.write(folder_name_without_head + "\n")

time.sleep(3)  # Pause for 5 seconds

line_numbers = []  # Create an empty list to record the reserved line numbers
new_lines = []  # Create an empty list to store lines that do not need to be deleted

# Open the txt file and examine it line by line
with open(f"final_data/{mode}_exist_demo5_folder.txt", "r") as exist_file, open(f"input_data/{mode}.files", "r") as file:
    exist_lines = [line.rstrip('\n') for line in exist_file.readlines()]  # Converts the contents of the exist_file to a list
    for line_num, line in enumerate(file, 1):  # Use enumerate() to get the line number, counting from 1
        line = line.strip()  # Remove line breaks and Spaces at the end of the line

        if mode == "dev":
            line_name_without_head= line[4:] # Remove the train/ dev/ test/ at the beginning of each line
        elif mode == "test":
            line_name_without_head= line[5:] # Remove the train/ dev/ test/ at the beginning of each line
        elif mode == "train":
            line_name_without_head= line[6:] # Remove the train/ dev/ test/ at the beginning of each line
        
        if line_name_without_head in exist_lines:
            print(f"A matching string was found")
            line_numbers.append(line_num)  # Records the number of the reserved row
        else:
            print(exist_lines)
            print(line_name_without_head + " dir didn't have demo5.txt, so will be delete.\n")

print(f"被保留的行号是{line_numbers}")

# Create a temporary file to hold the reserved lines for file name deletion
temp_filename1 = tempfile.NamedTemporaryFile(delete=False).name
with open(f"input_data/{mode}.files", "r") as file, open(temp_filename1, "w") as temp_file:
    for line_num, line in enumerate(file, 1):
        if line_num in line_numbers:
            temp_file.write(line)

# Overwrite the temporary file over the original file
shutil.move(temp_filename1, f"final_data/{mode}.files")


# Create a temporary file to hold the reserved lines for line deletion
temp_filename2 = tempfile.NamedTemporaryFile(delete=False).name
with open(f"input_data/{mode}.text", "r") as file, open(temp_filename2, "w") as temp_file:
    for line_num, line in enumerate(file, 1):
        if line_num in line_numbers:
            temp_file.write(line)

# Overwrite the temporary file over the original file
shutil.move(temp_filename2, f"final_data/{mode}.text")



