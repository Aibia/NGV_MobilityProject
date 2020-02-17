import os
import cv2
import time
from datetime import datetime
from client.vision import utils
from client.vision.cascade import haar
from client import logger, config

CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
YML_DIR_PATH = os.path.join(CURRENT_DIR_PATH, 'ymls')
TODAY = datetime.now().strftime('%Y-%m-%d')

def find_patient():
    """
    
    :returns:
    """
    face = haar.find_face()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer_path = utils.get_latest_yml_path()
    if os.path.exists(recognizer_path) == False:
        logger.log.error("[vision/recognizer.py:find_patient][E] " + \
            "No Such File : {}".format(recognizer_path))
        return -1, "-1"
    recognizer.read(recognizer_path)
    if config.DISPLAY_ON:
        cv2.imshow('face', face)
        time.sleep(1)
    cv2.destroyAllWindows()
    id, confidence = recognizer.predict(face)
    return id, "{}".format(round(100-confidence))
