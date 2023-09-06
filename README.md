# Celebrity-Face-Detection with Recognition

## Project Description
- The project uses a combination of face detection and face recognition algorithms to identify specific celebrities in videos. 
- It uses the OpenCV library to identify the faces in each frame of the video.
- A Pre-trained CNN model or cascade classifiers to match the detected faces to a database (generated using selenium for Google images and API for Bing images) of celebrity faces.
- It then iterates over each frame in the video stream. For each frame, it uses the model to detect any faces in the frame.
- If a face is detected, it draws a bounding box around the face with name and blur the unknown faces.

## Conclusion
- On comparing face detection model i.e. Haar Cascade and MTCNN we concluded that haar cascade is much faster that MTCNN but it detect faces with less accuracy, So, if high computation hardware is available MTCNN is recommended.
- On comparing two feature extraction model i.e. FaceNet and VGG16, VGG16 predicts with more accuracy.


