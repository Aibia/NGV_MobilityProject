import os
import cv2
import time
from gpiozero import LED
from aiy.pins import LED_1
from client import logger
## LED_1 is on when camera is finding a face
## LED_2 is on when camera captures a face

CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
OPEN_CV_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "opencv-data")
HAAR_CASCADE_DIR_PATH = os.path.join(OPEN_CV_DIR_PATH, "haarcascades")
FACE_CASCADE_XML_PATH = os.path.join(HAAR_CASCADE_DIR_PATH, "haarcascade_frontalcatface.xml")
EYE_CASCADE_XML_PATH = os.path.join(HAAR_CASCADE_DIR_PATH, "haarcascade_eye.xml")

	
def find_face(GRAY=True, display=False, save=False):
    try:
        display=True
        face_cascade = cv2.CascadeClassifier(FACE_CASCADE_XML_PATH)
        cap = cv2.VideoCapture(0)
        led_1 = LED(LED_1)
        logger.log.info("Start to find a face ...")
        led_1.on()
        while True:
            # Read the frame
            ## TODO
            ## GPIO ERROR SOLVING
            #led_1.blink(0.1,0.1,2)
            #time.sleep(0.2)
            _, img = cap.read()
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect the faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            if len(faces) > 0:
                #led_2.blink(0.2,0.2,2)
                #time.sleep(0.4)
                break
            elif display and GRAY:
                cv2.imshow('camera', gray)
            elif display:
                cv2.imshow('camera', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        led_1.off()
        cap.release()
        if display:
            cv2.destroyAllWindows()

        if GRAY:
            for (x, y, w, h) in faces:
                gray = gray[y:y+h, x:x+w]
            img = gray
        else:
            for (x, y, w, h) in faces:
                img = img[y:y+h, x:x+w]
    except Exception as e:
        logger.log.debug("Error " + str(e))
        return []
    else:
        return img