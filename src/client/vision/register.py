from cascade import haar
import random
import os
from datetime import datetime


CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
TEMP_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "temp")
YML_DIR_PATH = os.path.join(CURRENT_DIR_PATH, 'ymls')
TODAY = datetime.now().strftime('%Y-%m-%d') 

def train_recognizer(datasets, recognizer_path=os.path.join(YML_DIR_PATH, '{}.yml'.format(TODAY))):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if os.path.exists(recognizer_path):
        recognizer.read(recognizer_path)
    recognizer.train(datasets["faces"], datasets["ids"]) 
    recognizer.write(recognizer_path) 
    return True

def register_patient():
    ## TODO 
    ## 랜덤한 값 생성
    id_ = random.randint(1, 10)
    datasets = {
        "faces" : [],
        "ids" : [id_] * 10
    }
    for i in range(10):
        face = haar.find_face()
        datasets["faces"].append(face)
    return train_recognizer(datasets)
