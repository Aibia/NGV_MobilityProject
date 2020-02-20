#-*- coding:utf-8 -*-
import os
import cv2
import numpy
import time
from client import logger, config
from aiy.board import Board, Led

CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
OPEN_CV_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "opencv-data")
HAAR_CASCADE_DIR_PATH = os.path.join(OPEN_CV_DIR_PATH, "haarcascades")
FACE_CASCADE_XML_PATH = os.path.join(HAAR_CASCADE_DIR_PATH, "haarcascade_frontalface_default.xml")
EYE_CASCADE_XML_PATH = os.path.join(HAAR_CASCADE_DIR_PATH, "haarcascade_eye.xml")

DISPLAY_ON = config.DISPLAY_ON
DISPLAY_COLOR_ON = config.DISPLAY_COLOR_ON


def get_gray_face(frame:numpy.ndarray)->numpy.ndarray:
    """그레이 스케일된 이미지에서 얼굴부분을 크롭해 반환한다.
    
    :param numpy.ndarray frame: 얼굴을 찾고자 하는 그레이스케일된 이미지 파일
    :returns numpy.ndarray: 찾아진 얼굴 
    """
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_XML_PATH)
    faces = face_cascade.detectMultiScale(frame, 1.3, 5, minSize=(30, 30))
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            return frame[y:y+h, x:x+w]
    return numpy.ndarray([])


def find_face()->numpy.ndarray:
    """실시간으로 얼굴을 찾아서 반환함

    :returns numpy.ndarray: 찾아진 그레이 스케일 된 얼굴 이미지 데이터
    """
    try:
        img = []
        face = []
        face_cascade = cv2.CascadeClassifier(FACE_CASCADE_XML_PATH)
        cap = cv2.VideoCapture(0)
        while True:
            # Read the frame
            _, frame = cap.read()
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect the faces
            tmp_faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))
    
            for(x, y, w, h) in tmp_faces:
                if DISPLAY_ON and DISPLAY_COLOR_ON == False:
                    gray = cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 255, 0), 2)
                elif DISPLAY_ON and DISPLAY_COLOR_ON:
                    frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

            if DISPLAY_ON:
                cv2.imshow('camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if len(tmp_faces) > 0:
                face = gray[y:y+h, x:x+w]
                break
        cap.release()
        if DISPLAY_ON:
            cv2.destroyAllWindows()
    except Exception as e:
        logger.log.error("[vision/cascade/haar.py:find_face][E] {}".format(e))
        return numpy.adarray([])
    else:
        return face

        
        
        
