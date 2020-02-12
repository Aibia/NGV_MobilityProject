import os
import logging
from datetime import datetime
from client import config

LOG_DIR_PATH = config.LOG_DIR_PATH
TODAY = datetime.now().strftime('%Y-%m-%d') 


class Logger:
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super( Logger, self).__new__(self)
        return self.instance

    def __init__(self):
        if os.path.exists(LOG_DIR_PATH) == False:
            os.mkdir(LOG_DIR_PATH)
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] > %(message)s')
        file_handler = logging.FileHandler(os.path.join(LOG_DIR_PATH, '{}.log'.format(TODAY)))
        file_handler.setFormatter(formatter)
        self.__logger.addHandler(file_handler)
    

    def info(self, text):
        return self.__logger.info(text)


    def warning(self, text):
        return self.__logger.warning(text)


    def debug(self, text):
        return self.__logger.debug(text)


log = Logger()