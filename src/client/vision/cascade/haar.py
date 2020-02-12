import os
import cv2
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
CHECK_FACE_TIME_OUT = config.CHECK_FACE_TIME_OUT

def get_faces():
    try:
        faces = []
        face_cascade = cv2.CascadeClassifier(FACE_CASCADE_XML_PATH)
        cap = cv2.VideoCapture(0)
        while True:
            # Read the frame
            _, frame = cap.read()
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect the faces
            tmp_faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            for(x, y, w, h) in tmp_faces:
                if DISPLAY_COLOR_ON:
                    img = frame[y:y+h, x:x+w]
                else:
                    img = gray[y:y+h, x:x+w]
                faces.append(img)
            if len(faces) > 0:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
    except Exception as e:
        logger.log.debug("Error " + str(e))
        return []
    else:
        return faces

def find_face():
    face = []
    with Board() as board:
        while face == []:
            for tmp_face in get_faces():
                if DISPLAY_ON:
                    cv2.imshow('face', tmp_face)
                time.sleep(10)
                board.led.state = Led.ON
                if board.button.wait_for_press(CHECK_FACE_TIME_OUT):
                    face = tmp_face
                board.led.state = Led.OFF
            if DISPLAY_ON:
                cv2.destroyAllWindows()
    return face
        
        
        
