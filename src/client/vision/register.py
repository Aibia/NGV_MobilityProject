import os
import cv2
import numpy
from datetime import datetime
from client.db import database
from client.vision import utils
from client.vision.cascade import haar
from client import config, logger


CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
TEMP_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "temp")
YML_DIR_PATH = os.path.join(CURRENT_DIR_PATH, 'ymls')
TODAY = datetime.now().strftime('%Y-%m-%d') 
TAKE_PIC_TIMES = config.TAKE_PIC_TIMES

def train_recognizer(datasets, recognizer_path=os.path.join(YML_DIR_PATH, '{}.yml'.format(TODAY)), OLD_RECOGNIZER=True):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if OLD_RECOGNIZER:
        OLD_RECOGNIZER_PATH = utils.get_latest_yml_path()
        if OLD_RECOGNIZER_PATH != "" and os.path.exists(OLD_RECOGNIZER_PATH):
            recognizer.read(OLD_RECOGNIZER_PATH)
    elif os.path.exists(recognizer_path):
        recognizer.read(recognizer_path)
    recognizer.train(datasets["faces"], datasets["ids"]) 
    recognizer.write(recognizer_path) 
    return database.save_new_patient(datasets["ids"][0])

def register_patient():
    new_id = utils.create_new_id()
    datasets = {
        "faces" : [],
        "ids" : numpy.array([new_id] * TAKE_PIC_TIMES)
    }
    logger.log.info("new patient id is "+ str(new_id))
    for i in range(1, TAKE_PIC_TIMES+1):
        face = haar.find_face()
        logger.log.info("Take "+str(i))
        datasets["faces"].append(face)
    logger.log.info("taking a pic is finished")
    return train_recognizer(datasets)
