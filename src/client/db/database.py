import csv
import time
from client.voice import tts, stt
from client import config

PATIENT_INFO_CSV_PATH = config.PATIENT_INFO_CSV_PATH
MEDICINE_INFO_CSV_PATH = config.MEDICINE_INFO_CSV_PATH

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
    field_names = patient_info.keys()
    with open(PATIENT_INFO_CSV_PATH, 'a') as fd:
        csv_dict_fd = csv.DictWriter(fd, fieldnames=field_names)
        csv_dict_fd.writerow(patient_info)
    return True


def save_medicine_info(patient_id, medicine_info):
    field_names = medicine_info.keys()
    with open(MEDICINE_INFO_CSV_PATH, 'a') as fd:
        csv_dict_fd = csv.DictWriter(fd, fieldnames=field_names)
        csv_dict_fd.writerow(medicine_info)
    return True
    
    
def save_new_patient(patient_id):
    tts.say("Tell me what is your name?")
    name = stt.google_stt()
    count = 0
    while name == "":
        if count == 10:
            tts.say('error')
            break
        tts.say("I didn't understand")
        time.sleep(1)
        tts.say("What is your name?")
        name = stt.google_stt()
        count += 1
    count = 0
    tts.say("what is you age?")
    age = stt.google_stt()
    while age == "":
        if count == 10:
            tts.say('error')
            break
        tts.say("I didn't understand")
        time.sleep(1)
        tts.say("What is your age?")
        age = stt.google_stt()
        count += 1
    return save_patient_info(patient_id, {"id":patient_id, "name":name, "age":age}), save_medicine_info(patient_id, {"id":patient_id, "medicine1":0, "medicine2":1, "medicine3":0})