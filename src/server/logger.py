import logging
import os
from datetime import datetime
from server import config

LOG_DIR_PATH = config.LOG_DIR_PATH
TODAY = datetime.now().strftime('%Y-%m-%d') 


class Logger:
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super( Logger, self).__new__(self)
        return self.instance

    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] (%(filename)s:%(lineno)d) > %(message)s')
        file_handler = logging.FileHandler(os.path.join(LOG_DIR_PATH, '{}.log'.format(TODAY)))
        file_handler.setFormatter(formatter)
        self.__logger.addHandler(file_handler)
    

    def info(self):
        return self.__logger.info


    def warning(self):
        return self.__logger.warning


    def debug(self):
        return self.__logger.debug


log = Logger()