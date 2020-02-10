import os
from datetime import datetime
from client.db import database
from client.vision import utils
from client.vision.cascade import haar


CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
TEMP_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "temp")
YML_DIR_PATH = os.path.join(CURRENT_DIR_PATH, 'ymls')
TODAY = datetime.now().strftime('%Y-%m-%d') 

def train_recognizer(datasets, recognizer_path=os.path.join(YML_DIR_PATH, '{}.yml'.format(TODAY)), OLD_RECOGNIZER=True):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if OLD_RECOGNIZER:
        OLD_RECOGNIZER_PATH = utils.get_latest_yml_path()
        if OLD_RECOGNIZER_PATH != "":
            recognizer.read()
    elif os.path.exists(recognizer_path):
        recognizer.read(recognizer_path)
    recognizer.train(datasets["faces"], datasets["ids"]) 
    recognizer.write(recognizer_path) 
    return database.save_new_patient(datasets["ids"][0])

def register_patient():
    TAKE_PIC_TIMES = 10
    datasets = {
        "faces" : [],
        "ids" : [util.create_new_id()] * TAKE_PIC_TIMES
    }
    for i in range(TAKE_PIC_TIMES):
        face = haar.find_face()
        datasets["faces"].append(face)
    return train_recognizer(datasets)
