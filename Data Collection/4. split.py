import os
from sklearn.model_selection import train_test_split
import shutil

# Source directory path for cropped images
input_folder = 'crop_images'

# Output directory path for the split dataset
output_folder = 'Image_dataset'

# Create output directories for training and validation sets
train_folder = os.path.join(output_folder, 'train')
val_folder = os.path.join(output_folder, 'val')

os.makedirs(train_folder, exist_ok=True)
os.makedirs(val_folder, exist_ok=True)

# List all image files in the input folder
image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

# Split the dataset into training and validation sets
train_files, val_files = train_test_split(image_files, test_size=0.3, random_state=42)

# Copy images to the respective output folders
for file in train_files:
    src_path = os.path.join(input_folder, file)
    dst_path = os.path.join(train_folder, file)
    shutil.copy(src_path, dst_path)

for file in val_files:
    src_path = os.path.join(input_folder, file)
    dst_path = os.path.join(val_folder, file)
    shutil.copy(src_path, dst_path)



