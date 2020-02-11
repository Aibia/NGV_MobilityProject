from client.db import database
from client.vision import recognizer, register
from client.sensor import servomotor, request
from client.voice import tts, stt
from client import logger, config

SERVER_IP_ADDR = config.SERVER_IP_ADDR

def register_patient():
    return register.register_patient()

def main():
    register_patient()
    logger.log.info("Start running client app")
    
    while True:
        # 환자 얼굴 찾기
        logger.log.info("Start to find a face ...")
        patient_id = recognizer.find_patient()
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
