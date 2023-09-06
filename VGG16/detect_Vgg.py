# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 16:56:01 2023

@author: HP
"""
from PIL import Image
import numpy as np
import cv2
import pickle
from tensorflow.keras.models import load_model

# for face detection
face_cascade = cv2.CascadeClassifier(
    'haarcascade_frontalface_default.xml')


# size of the image to predict
image_width = 224
image_height = 224

# load the trained model
model = load_model('model_vgg.h5')

# the labels for the trained model
with open("ResultsMap.pkl", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {key:value for key,value in og_labels.items()}
    print(labels)


stream = cv2.VideoCapture('7.mp4')

while(True):
    # Capture frame-by-frame
    (grabbed, frame) = stream.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # try to detect faces in the webcam
    faces = face_cascade.detectMultiScale(
        rgb, scaleFactor=1.3, minNeighbors=5)

    # for each faces found
    for (x, y, w, h) in faces: 
        roi_rgb = rgb[y:y+h, x:x+w]

        # Draw a rectangle around the face
        color = (255, 0, 0) # in BGR
        stroke = 2
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, stroke)

        # resize the image
        size = (image_width, image_height)
        resized_image = cv2.resize(roi_rgb, size)
        image_array = np.array(resized_image, "uint8")
        img = image_array.reshape(1,image_width,image_height,3) 
        img = img.astype('float32')
        img /= 255
      
        # predict the image
        predicted_prob = model.predict(img)
        
        # Display the label
        font = cv2.FONT_HERSHEY_SIMPLEX
        name = labels[predicted_prob[0].argmax()]
        color = (255, 0, 255)
        stroke = 2
        cv2.putText(frame, f'({name})', (x,y-8),
            font, 1, color, stroke, cv2.LINE_AA)




        # Show the frame
        cv2.imshow("Image", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):    # Press q to break out of the loop
            break      

# Cleanup
stream.release()
cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)

