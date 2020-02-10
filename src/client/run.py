from db import database
from vision import recognizer
from sensor import servomotor, request
from voice import tts, stt
from . import logger, config

SERVER_IP_ADDR = config.SERVER_IP_ADDR

def main():
    
    logger.log.info("start running client app")

    while True:
        # 환자 얼굴 찾기
        logger.log.info()
        patient_id = recognizer.find_patinet()
        # 주행 멈추기 
        request.gpio_pin_change_out(SERVER_IP_ADDR)
        # 환자 정보 갖고오기 
        patient_info = database.get_patient_info(patient_id)
        medicine_info = database.get_medicine_info(patient_id)
        tts.say("Hello {}".format(patient_info["name"]))
        # 약 배출 
        servomotor.medicine_out(medicine_info)
        request.gpio_pin_change_in(SERVER_IP_ADDR)


if __name__ == "__main__":
    main()
