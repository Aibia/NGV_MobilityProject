import os
import time
import subprocess
from multiprocessing import Process
from aiy.board import Board, Led
from client.db import database
from client.vision import recognizer
from client.sensor import servomotor, request
from client.voice import tts, stt
from client import logger, config


class Client:
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super( Client, self).__new__(self)
        return self.instance


    def __init__(self):
        self.__web_server_proc = Process(target=(self.__webserver__))
        self.__nasa_proc = Process(target=self.__nasa__)


    def __webserver__(self):
        # TODO
        #if self.__web_server_proc.is_alive():
        #    logger.log.error("[run_client.py:__webserver__][E] Client is running")
        #    return False

        with Board() as board:
            proc = subprocess.Popen(['python3', config.APP_PATH])
            time.sleep(5)
            board.led.state = Led.ON
        return True 


    def __nasa__(self): 
        # TODO
        #if self.__nasa_proc.is_alive():
        #    logger.log.error("[run_client.py:__nasa__][E] Client is already running")
        #    return False

        logger.log.info("[run_client.py:__nasa__] Start running client app")
        if request.get_gpio_pin_function() == "out":
            logger.log.info("[run_client.py:__nasa__] Car Runnin")
            request.gpio_pin_change_in()
            
        while True:
            try:
                # 환자 얼굴 찾기
                patient_id = recognizer.find_patient()
                if patient_id == "":
                    continue
                logger.log.info("[run_client.py:__nasa__] Patient Found patient_id : {}".format(patient_id))
                # 주행 멈추기 
                logger.log.info("[run_client.py:__nasa__] Stop running ...")
                ret = request.gpio_pin_change_out()
                time.sleep(3)
                if ret == False:
                    logger.log.error("[run_client.py:__nasa__][E] Can't Stop Running")
                    request.gpio_pin_change_in()
                    continue
                # 환자 정보 갖고오기 
                patient_info = database.get_patient_info(patient_id)
                medicine_info = database.get_medicine_info(patient_id)
                if patient_info['name'] == "":
                    logger.log.error("[run_client.py:__nasa__][E] No Patient Found {}".format(patient_id))
                    time.sleep(3)
                    request.gpio_pin_change_in()
                    continue
                if config.CLOUD_TTS_ON:
                    tts.clova_tts("안녕하세요 {}님".format(patient_info["name"]))
                else:
                    tts.say("안녕하세요 {}님".format(patient_info["name"]))
                # 약 배출 
                servomotor.medicine_out(medicine_info)
                time.sleep(3)
                request.gpio_pin_change_in()
            except Exception as e:
                logger.log.error("[run_client.py:__nasa__][E] {}".format(e))


    def is_alive(self):
        return self.__nasa_proc.is_alive()

    
    def is_car_running(self):
        if request.get_gpio_pin_function() == "out":
            return False
        return True

    
    def start(self):
        #self.__web_server_proc.start()
        self.__nasa_proc.start()
        return True


    def stop(self, sig, frame):
        if self.__web_server_proc.is_alive():
            os.kill(self.__web_server_proc.pid, 9)
            logger.log.info("[run_client.py:stop] Web Server Stopped!")
            with Board() as board:
                board.led.state = Led.OFF
        if self.__nasa_proc.is_alive():
            self.__nasa_proc.terminate()
            logger.log.info("[run_client.py:stop] NASA App Stopped!")
        return True