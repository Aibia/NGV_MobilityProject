import os
import cv2

CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
TEMP_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "temp")

def train_recognizer(datasets, recognizer_path):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if os.path.exists(recognizer_path):
        recognizer.read(recognizer_path)
    recognizer.train(datasets["faces"], datasets["ids"]) 
    recognizer.write(recognizer_path) 
    return True


def get_id(img, recognizer_path):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    font = cv2.FONT_HERSHEY_SIMPLEX
    assert os.path.exists(recognizer_path)
    recognizer.read(recognizer_path)
    id, confidence = recognizer.predict(img)
    return id, "{}".format(round(100-confidence))
