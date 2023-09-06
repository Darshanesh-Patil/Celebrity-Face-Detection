import cv2
import os

# Haar cascade classifier file path
face_cascade_path = "haarcascade_frontalface_alt.xml"

# Source directory path
dataset_path = "downloaded_images"

# Destination directory path
destination_path = "face_crop_dataset1"

# Create the destination directory if it does not exist
if not os.path.exists(destination_path):
    os.mkdir(destination_path)

# Iterate over all images in the dataset directory
for image_path in os.listdir(dataset_path):
    # Read the image
    image = cv2.imread(os.path.join(dataset_path, image_path))

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = cv2.CascadeClassifier(face_cascade_path).detectMultiScale(gray_image)

    # Crop the faces and save them to the destination directory
    for (x, y, w, h) in faces:
        cropped_face = image[y:y+h, x:x+w]
        cv2.imwrite(os.path.join(destination_path, image_path), cropped_face)

