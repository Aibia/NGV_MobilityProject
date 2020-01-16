import cv2
import os
import numpy as np
from PIL import Image
from cascade import haar as h
import recognizer as r


def save_30(patient_id):
    PIC_NUM = 30
    if os.path.exists('temp/{}'.format(patient_id)) == False:
        os.mkdir('temp/{}'.format(patient_id))
    for _ in range(PIC_NUM):
        img = h.find_gray_face()
        cv2.imwrite('temp/{}/{}.jpg'.format(patient_id, _), img)


def train(patient_id):
    path = 'temp/{}'.format(patient_id)
    imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
    facesamples = []
    ids = []
    for imagepath in imagepaths:
        PIL_img = Image.open(imagepath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')
        id = patient_id 
        facesamples.append(img_numpy)
        ids.append(id)

    datasets = {
	"faces" : np.asarray(facesamples),
	"ids" : np.asarray(ids)
    }

    r.train_recognizer(datasets, "temp/train.yml")


def test():
    for _ in range(30):
        gray = h.find_gray_face()
        id, confidence = r.get_id(gray,'temp/train.yml' )
        print ('{} {}'.format(id, confidence))
PATIENT_ID = 19931102
#save_30(PATIENT_ID) 
#train(PATIENT_ID)
test()
