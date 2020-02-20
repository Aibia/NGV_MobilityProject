#-*- coding:utf-8 -*-
import time
import threading
import cv2
import numpy
import io
import picamera
from PIL import Image
from client.vision.cascade import haar

class Camera(object):
    """
    """
    thread = None
    frame = None
    last_access = 0

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(Camera, self).__new__(self)
        return self.instance


    def initialize(self):
        if Camera.thread is None:
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            while self.frame is None:
                time.sleep(0)


    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame
        
    
    @classmethod
    def capture(cls):
        return cls.frame


    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            camera.resolution = (400, 400)
            camera.hflip = True
            camera.vflip = False

            time.sleep(1.5)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):

                stream.seek(0)
                cls.frame = stream.read()
                stream.seek(0)
                stream.truncate()

                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None


