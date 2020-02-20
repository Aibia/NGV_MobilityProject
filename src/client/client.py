#-*- coding:utf-8 -*-
import os
import time
import signal
from multiprocessing import Process
from aiy.board import Board, Led
from client.db import database
from client.vision import recognizer
from client.sensor import servomotor, request
from client.voice import tts, stt
from client.html.app import app
from client import logger, config


class Client:
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super( Client, self).__new__(self)
        return self.instance


    def __init__(self):
        self.__web_server_proc = Process(target=(self.__webserver__))
        self.__nasa_proc = Process(target=self.__nasa__)
        signal.signal(signal.SIGINT, self.stop)


    def __webserver__(self):
        ## TODO STDOUT -> LOGGING
        with Board() as board:
            board.led.state = Led.ON
            app.run(host=config.HOST_IP_ADDR, debug=False, threaded=True)
            board.led.state = Led.OFF
        return True 


    def __nasa__(self): 
        logger.log.info("[run_client.py:__nasa__] Start running client app")
        if request.get_gpio_pin_function() == "out":
            logger.log.info("[run_client.py:__nasa__] Start Car Running")
            request.gpio_pin_change_in()
            
        while True:
            try:
                # 환자 얼굴 찾기
                patient_id = recognizer.find_patient()
                if patient_id == "-1" or database.has_patient_id(patient_id) == False:
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
                elif config.TTS_ON:
                    tts.say("안녕하세요 {}님".format(patient_info["name"]))
                # 약 배출 
                servomotor.medicine_out(medicine_info)
                time.sleep(3)
                request.gpio_pin_change_in()
            except Exception as e:
                logger.log.error("[run_client.py:__nasa__][E] {}".format(e))


    def is_web_running(self)->bool:
        """웹서버가 작동중인지의 여부를 확인할 수 있는 함수 

        :returns bool: 웹 서버가 작동중일 경우 True를 반환한다.
        """
        return self.__web_server_proc.is_alive()

    
    def is_nasa_running(self)->bool:
        """차량이 작동중인지의 여부를 확인할 수 있는 함수 
        서버에 리퀘스트를 보내 정해진 gpio값의 상태가 "out"인 경우 차량이 움직이고 있다고 판단한다.

        :returns bool: 차량이 작동중일 경우 True를 반환한다.
        """
        if request.get_gpio_pin_function() == "out":
            return False
        return True

    
    def start(self)->bool:
        """(main함수)웹서버와 얼굴인식 및 서보를 동작시킨다. 

        :returns bool: 실행 결과 
        """
        current_time = time.time()
        web_flag = False
        while time.time() - current_time < config.CONNECTION_TIME_OUT:
            web_flag = request.is_webserver_up()
            if web_flag:
                break

        if web_flag == False:
            logger.log.error("[client.py:start] Server is not connected")
            return False

        web_server_flag = self.__web_server_proc.is_alive()
        nasa_flag = self.__nasa_proc.is_alive()
        if web_server_flag and nasa_flag:
            logger.log.debug("[client.py:start] Web Server And NASA Already Running")
            return False
        if web_server_flag == False:
            self.__web_server_proc.start()
        if nasa_flag == False:
            self.__nasa_proc.start()
        
        if web_server_flag:
            logger.log.debug("[client.py:start] Web Server Already Running")
        elif nasa_flag:
            logger.log.debug("[client.py:start] NASA Already Running")
        if self.__web_server_proc.is_alive() == False and self.__nasa_proc.is_alive() == False:
            return False
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

