from client.db import database
from client.vision import recognizer, register
from client.sensor import servomotor, request
from client.voice import tts, stt
from client import logger, config


def register_patient():
    return register.register_patient()

def main():
    register_patient()
    logger.log.info("Start running client app")
    
    while True:
        # 환자 얼굴 찾기
        patient_id = recognizer.find_patient()

        # 주행 멈추기 
        logger.log.info("Patient found Stop running ")
        ret = request.gpio_pin_change_out()
        if ret == False:
            logger.log.debug("Error Can't Stop Running")
        # 환자 정보 갖고오기 
        patient_info = database.get_patient_info(patient_id)
        medicine_info = database.get_medicine_info(patient_id)
        tts.say("Hello {}".format(patient_info["name"]))
        # 약 배출 
        servomotor.medicine_out(medicine_info)
        request.gpio_pin_change_in()


if __name__ == "__main__":
    main()
