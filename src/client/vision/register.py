import os
import cv2
import numpy
from datetime import datetime
from client.db import database
from client.vision import utils
from client.vision.cascade import haar
from client import config, logger


CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
YML_DIR_PATH = os.path.join(CURRENT_DIR_PATH, 'ymls')
TODAY = datetime.now().strftime('%Y-%m-%d') 


def train_recognizer(datasets:dict, recognizer_path:str=os.path.join(YML_DIR_PATH, '{}.yml'.format(TODAY)), old_recognizer:bool=True):
    """데이터를 바탕으로 얼굴 정보를 학습시킨다. 
    학습된 YML파일은 recognizer_path에 저장되며 OLD_RECOGNIZER에 따라 이전 파일에 추가할 수 있다.

    :param dict datasets: 학습시킬 데이터셋
    :param str recognizer_path: 학습된 YML파일을 저장할 경로
    :param bool old_recognizer: 이전파일에 추가적으로 학습시킬때 사용되는 flag 
    이값이 참일 경우 recognizer_path는 자동으로 가장 최근의 YML파일의 경로로 바뀐다.
    :returns bool:
    """
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if old_recognizer:
        OLD_RECOGNIZER_PATH = utils.get_latest_yml_path()
        if OLD_RECOGNIZER_PATH != "" and os.path.exists(OLD_RECOGNIZER_PATH):
            recognizer.read(OLD_RECOGNIZER_PATH)
    elif os.path.exists(recognizer_path):
        recognizer.read(recognizer_path)
    recognizer.train(datasets["faces"], datasets["ids"]) 
    recognizer.write(recognizer_path) 
    return True


def train(patient_id:str, data_path:str)->bool:
    """환자의 얼굴을 인식시키기 위해 아이디별로 이미지를 학습시킨다.

    :param str patient_id: 학습시킬 환자의 아이디
    :param str data_path: 학습시킬 환자의 이미지가 저장되어있는 경로
    :returns bool:
    """
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

