import csv
import time
import string
import random
from client.voice import tts, stt
from client import config

PATIENT_INFO_CSV_PATH = config.PATIENT_INFO_CSV_PATH
MEDICINE_INFO_CSV_PATH = config.MEDICINE_INFO_CSV_PATH
ID_LENGTH = config.ID_LENGTH
NUMBER_STRING_POOL = "0123456789"
STR_STRING_POOL = string.ascii_lowercase
random.seed(0)

def create_random_number():
    RANDOM_STRING = ""
    for i in range(ID_LENGTH):
        RANDOM_STRING += random.choice(NUMBER_STRING_POOL)
    return RANDOM_STRING

def create_random_string(LENGTH):
    RANDOM_STRING = ""
    for i in range(LENGTH):
        RANDOM_STRING += random.choice(STR_STRING_POOL)
    return RANDOM_STRING

def create_new_id():
    ID = create_random_number()
    while has_patient_id(ID):
        ID = create_random_number()
    return int(ID)


def get_patient_info(patient_id):
    field_names = ["id", "name"]
    error = {}
    with open(PATIENT_INFO_CSV_PATH, 'r', encoding='utf-8') as fd:
        patients_csv = csv.DictReader(fd)
        field_names = patients_csv.fieldnames
        for patient in patients_csv:
            if patient['id'] == patient_id:
                return patient
    for field_name in field_names:
        error[field_name] = ""
    return error


def get_medicine_info(patient_id):
    field_names = ["id", "medicine1"]
    error = {}
    with open(MEDICINE_INFO_CSV_PATH, 'r', encoding='utf-8') as fd:
        csv_dict_fd = csv.DictReader(fd)
        field_names = csv_dict_fd.fieldnames
        for medicine_info in csv_dict_fd:
            if medicine_info['id'] == patient_id:
                return medicine_info
    for field_name in field_names:
        error[field_name] = ""
    return error


def has_patient_id(patient_id):
    if get_patient_info(patient_id)['id'] == '':
        return False
    return True


def save_patient_info(patient_id, patient_info):
    ## TODO
    ## 제대로 값이 헤더와 맞게 들어가지 않음 
    field_names = patient_info.keys()
    with open(PATIENT_INFO_CSV_PATH, 'a') as fd:
        csv_dict_fd = csv.DictWriter(fd, fieldnames=field_names)
        csv_dict_fd.writerow(patient_info)
    return True


def save_medicine_info(patient_id, medicine_info):
    ## TODO
    ## 제대로 값이 헤더와 맞게  들어가지 않음 
    field_names = medicine_info.keys()
    with open(MEDICINE_INFO_CSV_PATH, 'a') as fd:
        csv_dict_fd = csv.DictWriter(fd, fieldnames=field_names)
        csv_dict_fd.writerow(medicine_info)
    return True
    
    
def save_new_patient(patient_id):
    ## TODO
    ## 한글로 할껀지, 영어로 갈껀지, 외부 통신할껀지 정하기..
    #tts.say("Tell me what is your name?")
    tts.clova_tts("당신의 이름은 무엇인가요 ?")
    name = stt.clova_stt()
    count = 0
    while name == "":
        if count == 10:
            tts.say('error')
            break
        #tts.say("I didn't understand")
        tts.clova_tts("다시한번 말씀해주세요")
        time.sleep(1)
        #tts.say("What is your name?")
        tts.clova_tts("당신의 이름은 무엇인가요 ?")
        name = stt.clova_stt()
        count += 1
    count = 0
    #tts.say("what is you age?")
    tts.clova_tts("당신의 나이는 몇살인가요 ?")
    age = stt.clova_stt()
    while age == "":
        if count == 10:
            tts.say('error')
            break
        #tts.say("I didn't understand")
        tts.clova_tts("다시한번 말씀해주세요")
        time.sleep(1)
        #tts.say("What is your age?")
        tts.clova_tts("당신의 나이는 몇살인가요 ?")
        age = stt.clova_stt()
        count += 1
    return save_patient_info(patient_id, {"id":patient_id, "name":name, "age":age}), save_medicine_info(patient_id, {"id":patient_id, "medicine1":0, "medicine2":1, "medicine3":0})