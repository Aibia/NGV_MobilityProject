import voice
from vision import recognizer, cascade
import utils

RECOGNIZER_YML_PATH = "temp/train.yml"
def main():
    while True:
        # 주행
        gray_face = cascade.find_gray_face() 
        patient_id, confidence = recognizer.get_id(gray_face, RECOGNIZER_YML_PATH) 
        patient_name, drug = utils.get_patient_info(patient_id) 
        if patient_name != "":
            message = "hello... {} 약 제조 중 입니다.".format(patient_name)
            print (message)
            #voice.tts(message)
            # 약 제조 중
            # open door
                    
        


if __name__ == "__main__":
    main()
