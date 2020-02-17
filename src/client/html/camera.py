import time
import threading
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

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
        with PiCamera() as camera:
            camera.resolution = (400, 400)
            camera.hflip = True
            camera.vflip = False

            time.sleep(2)

            stream = PiRGBArray(camera, size=(400, 400))
            for frame in camera.capture_continuous(stream, 'bgr',
                                                 use_video_port=True):
                
                img = frame.array
                #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                #gray = cv2.equalizeHist(gray)
                
                vis = img.copy()
                cls.frame = vis.tobytes()

                stream.truncate(0)

                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
