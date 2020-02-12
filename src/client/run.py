import os
import signal
import time
import subprocess
from aiy.board import Board, Led
from client.db import database
from client.vision import recognizer
from client.sensor import servomotor, request
from client.voice import tts, stt
from client import logger, config

def html():
    with Board() as board:
        proc = subprocess.Popen(['python3', config.APP_PATH])
        time.sleep(5)
        board.led.state = Led.ON
        if board.button.wait_for_press():
            proc.kill()
        board.led.state = Led.OFF
    return True

def main():
    html()
    logger.log.info("Start running client app")
    
    while True:
        # 환자 얼굴 찾기
        patient_id = recognizer.find_patient()

        # 주행 멈추기 
        logger.log.info("Patient found Stop running ")
        ret = request.gpio_pin_change_out()
        #if ret == False:
        #    logger.log.debug("Error Can't Stop Running")
        # 환자 정보 갖고오기 
        patient_info = database.get_patient_info(patient_id)
        medicine_info = database.get_medicine_info(patient_id)
        tts.clova_tts("안녕하세요 {}님".format(patient_info["name"]))
        # 약 배출 
        servomotor.medicine_out(medicine_info)
        request.gpio_pin_change_in()


if __name__ == "__main__":
    main()
