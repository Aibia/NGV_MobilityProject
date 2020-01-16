import cv2
import os
import numpy as np
from PIL import Image
from cascade import haar as h
import recognizer as r


def save_30():
    PIC_NUM = 30
    for _ in range(PIC_NUM):
        img = h.find_gray_face()
        cv2.imwrite('temp/{}.jpg'.format(_), img)


def train():
    path = 'temp'
    imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
    facesamples = []
    ids = []
    for imagepath in imagepaths:
        PIL_img = Image.open(imagepath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')
        id = 1 
        facesamples.append(img_numpy)
        ids.append(id)

    datasets = {
	"faces" : np.asarray(facesamples),
	"ids" : np.asarray(ids)
    }

    r.train_recognizer(datasets, "temp/train.yml")


def test():
    gray = h.find_gray_face()
    id, confidence = r.get_id(gray,'temp/train.yml' )
    print ('{} {}'.format(id, confidence))
  
test()
