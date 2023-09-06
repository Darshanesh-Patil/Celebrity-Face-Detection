import face_recognition
import cv2
import os

# Source directory path for dataset images
dataset_path = "downloaded_images"

# Destination directory path
destination_path = "similar_faces_datasetv2"

# Directory path for reference images
reference_images_path = "reference_face"  # Replace with the path to your reference images directory

# Create the destination directory if it does not exist
if not os.path.exists(destination_path):
    os.mkdir(destination_path)

# Load reference images from the reference_images directory
reference_images = os.listdir(reference_images_path)
reference_face_encodings = []

for reference_image in reference_images:
    reference_image_path = os.path.join(reference_images_path, reference_image)
    reference_image = face_recognition.load_image_file(reference_image_path)
    reference_face_encoding = face_recognition.face_encodings(reference_image)[0]
    reference_face_encodings.append(reference_face_encoding)

# Define a similarity threshold (adjust as needed)
similarity_threshold = 0.6

# Counter for generating unique names
counter = 1

# Iterate over all images in the dataset directory
for image_path in os.listdir(dataset_path):
    # Read the image
    image = cv2.imread(os.path.join(dataset_path, image_path))

    # Find face locations and encodings in the image
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    for i, face_encoding in enumerate(face_encodings):
        # Compare the face encoding with reference encodings
        similarities = face_recognition.face_distance(reference_face_encodings, face_encoding)

        # Check if any similarity score is below the threshold
        if any(similarity < similarity_threshold for similarity in similarities):
            # Crop and save the face to the destination directory with a unique name
            top, right, bottom, left = face_locations[i]
            face_image = image[top:bottom, left:right]
            # Generate a unique filename based on the counter
            cropped_image_name = f"cropped_face_{counter}.jpg"
            counter += 1
            cv2.imwrite(os.path.join(destination_path, cropped_image_name), face_image)

# Release resources
cv2.destroyAllWindows()


