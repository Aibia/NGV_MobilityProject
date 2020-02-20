#-*- coding:utf-8 -*-
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
        if os.path.exists(LOG_DIR_PATH) == False:
            os.mkdir(LOG_DIR_PATH)
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] (%(filename)s:%(lineno)d) > %(message)s')
        file_handler = logging.FileHandler(os.path.join(LOG_DIR_PATH, '{}.log'.format(TODAY)))
        stream_handler = logging.StreamHandler()
        file_handler.setFormatter(formatter)
        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(stream_handler)
    

    def info(self, text):
        """기본 로깅 함수

        :param str text: 로깅할 문자
        :returns: 파일에 로깅
        """
        return self.__logger.info(text)


    def warning(self, text):
        """경고하기 위한 로깅
        
        :param str text: 로깅할 문자
        :returns: 파일에 로깅
        """
        return self.__logger.warning(text)


    def debug(self, text):
        """디버깅을 위한 로깅
        
        :param str text: 로깅할 문자
        :returns: 파일에 로깅
        """
        return self.__logger.debug(text)


    def error(self, text):
        """에러를 로깅
        
        :param str text: 로깅할 문자
        :returns: 파일에 로깅
        """
        return self.__logger.error(text)
    

log = Logger()