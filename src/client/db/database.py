import csv
import time
import string
import numpy
import random
from client.voice import tts, stt
from client.vision import register
from client import config, logger

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
    field_names = ['id', 'name', 'age']
    with open(PATIENT_INFO_CSV_PATH, 'a') as fd:
        csv_dict_fd = csv.DictWriter(fd, fieldnames=field_names)
        csv_dict_fd.writerow(patient_info)
    return True


def save_medicine_info(patient_id, medicine_info):
    field_names = ['id', 'medicine1', 'medicine2', 'medicine3']
    with open(MEDICINE_INFO_CSV_PATH, 'a') as fd:
        csv_dict_fd = csv.DictWriter(fd, fieldnames=field_names)
        csv_dict_fd.writerow(medicine_info)
    return True


def delete_patient_info(patient_id):
    field_names = ['id', 'name', 'age']
    patient_infos = []
    with open(PATIENT_INFO_CSV_PATH, 'r') as fd_in:
        csv_dict_reader = csv.DictReader(fd_in, fieldnames=field_names)
        for row in csv_dict_reader:
            if row['id'] != patient_id:
                patient_infos.append(row)
    with open(PATIENT_INFO_CSV_PATH, "w") as fd_out:
        csv_dict_writer = csv.DictWriter(fd_out, fieldnames=field_names)
        csv_dict_writer.writeheader()
        csv_dict_writer.writerows(patient_infos)
    return True


def delete_medicine_info(patient_id):
    field_names = ['id', 'medicine1', 'medicine2', 'medicine3']
    medicine_infos = []
    with open(MEDICINE_INFO_CSV_PATH, 'r') as fd_in:
        csv_dict_reader = csv.DictReader(fd_in, fieldnames=field_names)
        for row in csv_dict_reader:
            if row['id'] != patient_id:
                medicine_infos.append(row)
    with open(MEDICINE_INFO_CSV_PATH, 'w') as fd_out:
        csv_dict_writer = csv.DictWriter(fd_out, fieldnames=field_names)
        csv_dict_writer.writeheader()
        csv_dict_writer.writerows(medicine_infos)
    return True