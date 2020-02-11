import os
import cv2
from datetime import datetime
from client.vision import utils
from client.vision.cascade import haar
from client import logger

CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
TEMP_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "temp")
YML_DIR_PATH = os.path.join(CURRENT_DIR_PATH, 'ymls')
TODAY = datetime.now().strftime('%Y-%m-%d')
LATEST_YML_PATH = utils.get_latest_yml_path()


def find_patient(recognizer_path=LATEST_YML_PATH):
    ## TODO
    ## ERROR
    face = haar.find_face()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    font = cv2.FONT_HERSHEY_SIMPLEX
    logger.log.debug("recognizer_path : " + recognizer_path)
    assert os.path.exists(recognizer_path) == False
    recognizer.read(recognizer_path)
    id, confidence = recognizer.predict(face)
    return id, "{}".format(round(100-confidence))
