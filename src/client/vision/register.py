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
    return True

def train(patient_id, data_path):
    images = [os.path.join(data_path, f) for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path,f))]
    faces = []
    for image_path in images:
        face = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        face = haar.get_gray_face(face)
        if face != []:
            faces.append(numpy.asarray(face, dtype=numpy.uint8))
    if len(faces) == 0:
        return False
    labels = numpy.asarray([int(patient_id)] *len(faces))
    labels = numpy.asarray(labels)
    datasets = {
        "faces" : faces, 
        "ids" : labels
    }
    return train_recognizer(datasets)

