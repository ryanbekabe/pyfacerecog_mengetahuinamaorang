import cv2
import os
import numpy as np    #numpy for matrix calculations
from PIL import Image
def assure_path_exists(path):           #same as in face_dataset.py
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
recognizer = cv2.face.LBPHFaceRecognizer_create()       # Create Local Binary Patterns Histograms for face recognization
#recognizer = cv2.face_LBPHFaceRecognizer_create()       # Create Local Binary Patterns Histograms for face recognization
#For me changing createLBPHFaceRecognizer() to
#recognizer = cv2.face.EigenFaceRecognizer_create()
#cv2.face_LBPHFaceRecognizer
#EigenFaces – cv2.face.createEigenFaceRecognizer()
#FisherFaces – cv2.face.createFisherFaceRecognizer()
#Local Binary Patterns Histograms (LBPH) – cv2.face.createLBPHFaceRecognizer()

detector = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
def getImagesAndLabels(path):       #method to get the images and label data
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]      # Get all file path
    faceSamples=[]         # create empty face sample list
    ids = []               # create empty id list
    for imagePath in imagePaths:     # Loop for all the file path
        PIL_img = Image.open(imagePath).convert('L')    # Get the image and convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')       # PIL image to numpy array
        id = int(os.path.split(imagePath)[-1].split(".")[1])      # Get the image id
        faces = detector.detectMultiScale(img_numpy)  # Get the face from the training images
        for (x,y,w,h) in faces:   # Loop for each face, append to their respective ID
            faceSamples.append(img_numpy[y:y+h,x:x+w])        # Add the image to face samples
            ids.append(id)   # Add the ID to IDs
    return faceSamples,ids  
faces,ids = getImagesAndLabels('dataset\\')  # Get the faces and IDs
recognizer.train(faces, np.array(ids)) # Train the model using the faces and IDs
assure_path_exists('trainer\\')    # Save the model into trainer.yml
recognizer.save('trainer\\trainer.yml')