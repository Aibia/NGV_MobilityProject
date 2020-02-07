import os
import cv2

CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
OPEN_CV_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "opencv-data")
HAAR_CASCADE_DIR_PATH = os.path.join(OPEN_CV_DIR_PATH, "haarcascades")
FACE_CASCADE_XML_PATH = os.path.join(HAAR_CASCADE_DIR_PATH, "haarcascade_frontalcatface.xml")
EYE_CASCADE_XML_PATH = os.path.join(HAAR_CASCADE_DIR_PATH, "haarcascade_eye.xml")

	
def find_face(GRAY=True):
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_XML_PATH)
    cap = cv2.VideoCapture(0)
   
    while True:
        # Read the frame
        _, img = cap.read()
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) > 0:
            break
    cap.release()
    if GRAY:
        for (x, y, w, h) in faces:
            gray = gray[y:y+h, x:x+w]
        return gray

    for (x, y, w, h) in faces:
        img = img[y:y+h, x:x+w]
    return img
