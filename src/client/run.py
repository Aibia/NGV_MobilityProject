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

#signal.signal(signal.SIGINT, logger.log.info("Stop running app ..."))

def html():
    with Board() as board:
        proc = subprocess.Popen(['python3', config.APP_PATH])
        time.sleep(5)
        board.led.state = Led.ON
        if board.button.wait_for_press():
            os.kill(proc.pid, 9)
        board.led.state = Led.OFF
    return True
    

def main():
    html()
    logger.log.info("Start running client app")
    
    while True:
        # 환자 얼굴 찾기
        try:
            patient_id, confidence = recognizer.find_patient()
            if patient_id == -1:
                continue
            logger.log.info("Patient found patient_id : {} confidence : {}".format(patient_id, confidence))
            # 주행 멈추기 
            logger.log.info(" Stop running ...")
            ret = request.gpio_pin_change_out()
            time.sleep(10)
            if ret["status"] == False:
                logger.log.debug("Error Can't Stop Running")
                request.gpio_pin_change_in()
                continue
            # 환자 정보 갖고오기 
            patient_info = database.get_patient_info(patient_id)
            medicine_info = database.get_medicine_info(patient_id)
            if patient_info['name'] == "":
                logger.log.debug("No Patient Found {}".format(patient_id))
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
            logger.log.debug("{}".format(e))



if __name__ == "__main__":
    main()
