import os

# Set the path to the folder containing your images
folder_path = 'crop_images'

# List all files in the folder
files = os.listdir(folder_path)

# Define a prefix for the new filenames
new_filename_prefix = 'image'

# Iterate through the files and rename them
for i, filename in enumerate(files):
    # Check if the file is an image (you can customize this check)
    if filename.endswith(('.jpg', '.png', '.jpeg', '.gif')):
        # Create the new filename
        new_filename = f"{new_filename_prefix}{i+1}.jpg"  # You can change the file extension if needed

        # Construct the full path for the old and new filenames
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)

        # Check if the new filename already exists
        if os.path.exists(new_file_path):
            # If it does, you can add a number or other unique identifier to make it unique
            new_filename = f"{new_filename_prefix}{i+1}.jpg"
            new_file_path = os.path.join(folder_path, new_filename)

        # Rename the file
        os.rename(old_file_path, new_file_path)

print("Image renaming complete.")
