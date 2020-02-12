import os
import cv2
import numpy
import time
from client import logger, config
from aiy.board import Board, Led

CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
OPEN_CV_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "opencv-data")
HAAR_CASCADE_DIR_PATH = os.path.join(OPEN_CV_DIR_PATH, "haarcascades")
FACE_CASCADE_XML_PATH = os.path.join(HAAR_CASCADE_DIR_PATH, "haarcascade_frontalcatface.xml")
EYE_CASCADE_XML_PATH = os.path.join(HAAR_CASCADE_DIR_PATH, "haarcascade_eye.xml")

DISPLAY_ON = config.DISPLAY_ON
DISPLAY_COLOR_ON = config.DISPLAY_COLOR_ON

def save_gray_face(img_path):
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_XML_PATH)
    frame = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    faces = face_cascade.detectMultiScale(frame, 1.3, 5)
    if len(faces) == 1:
        for (x, y, w, h) in faces:
            cv2.imwrite(img_path, frame[y:y+h, x:x+w])
    else:
        cv2.imwrite(img_path, frame)
    return True


def find_face():
    try:
        img = []
        face = []
        face_cascade = cv2.CascadeClassifier(FACE_CASCADE_XML_PATH)
        cap = cv2.VideoCapture(0)
        while True:
            # Read the frame
            _, frame = cap.read()
            # Convert to grayscale
            gray = cv2.cvtColor(cv2.UMat(frame), cv2.COLOR_BGR2GRAY)
            # Detect the faces
            tmp_faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
            for(x, y, w, h) in tmp_faces:
                if DISPLAY_ON and DISPLAY_COLOR_ON == False:
                    gray = cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 255, 0), 2)
                elif DISPLAY_ON and DISPLAY_COLOR_ON:
                    frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

            if DISPLAY_ON:
                cv2.imshow('camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if len(tmp_faces) == 1:
                face = gray[y:y+h, x:x+w]
                break
        cap.release()
        if DISPLAY_ON:
            cv2.destroyAllWindows()
    except Exception as e:
        logger.log.debug("Error " + str(e))
        return []
    else:
        return face

        
        
        
