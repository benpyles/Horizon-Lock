#!/bin/bash

# 1. Ask for input
read -p "Enter start number (e.g., 0): " start_num
read -p "Enter end number (e.g., 19): " end_num
read -p "Enter destination folder name: " dest_folder

# 2. Create the folder if it doesn't exist
if [ ! -d "$dest_folder" ]; then
    mkdir -p "$dest_folder"
    echo "Created directory: $dest_folder"
fi

echo "--- Copying files ---"

# 3. Loop through the range
# "-f %04g" forces the numbers to be 4 digits with zero padding (e.g., 0 -> 0000)
count=0
for i in $(seq -f "%04g" "$start_num" "$end_num"); do
    filename="tile_${i}.png"

    if [ -f "$filename" ]; then
        mv "$filename" "$dest_folder/"
        ((count++))
    else
        echo "Warning: $filename not found, skipping."
    fi
done

echo "--- Done! Copied $count files to '$dest_folder' ---"