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

def find_patient()->str:
    """환자의 얼굴을 찾고 아이디를 반환한다.
    ymls 폴어 안에 있는 가장 최근의 학습 파일을 이용하여 환자의 얼굴을 찾는다.
    
    :returns str: 찾은 얼굴의 아이디 반환 환자가 아닐경우 빈 스트링값을 반환한다.
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
    id_, confidence = recognizer.predict(face)
    confidence = round(100-confidence)
    logger.log.info("[vision/recognizer.py:find_patient] " + \
        "** id : {}\tconfidence : {}".format(id_, confidence))
    if confidence < 0:
        return ""
    return id_
