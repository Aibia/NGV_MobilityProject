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
PATINET_INFO_FIELD_NAMES = ["id", "name", "age"]
MEDICINE_INFO_FIELD_NAMES = ["id", "medicine1", "medicine2", "medicine3"]
random.seed(0)

def create_random_number(length:int)->str:
    """랜덤한 숫자(문자열)를 생성해내는 함수 입니다.

    :param int length: 랜덤 숫자의 길이를 결정 짓는 int
    :returns str: 문자열 타입의 랜덤 숫자
    """
    result = ""
    number_string_pool_no_zero = "123456789"
    number_string_pool = "0123456789"
    for _ in range(length):
        if len(result) == 0:
            #0으로 시작하지 않는 문자형 랜덤 숫자를 만들기 위함
            result += random.choice(number_string_pool_no_zero)
        else:
            result += random.choice(number_string_pool)
    return result


def create_random_string(length:int)->str:
    """랜덤한 문자열을 생성해내는 함수 입니다.

    :param int length: 랜덤 숫자의 길이를 결정 짓는 int
    :returns str: 랜덤 문자열
    """
    str_string_pool = string.ascii_lowercase + string.ascii_uppercase
    result = ""
    for _ in range(length):
        result += random.choice(str_string_pool)
    return result


def create_new_id()->str:
    """config파일에 지정되어있는 ID길이에 맞는 환자 ID 생성

    :returns str: 문자형 환자 아이디
    """
    ID = create_random_number(ID_LENGTH)
    while has_patient_id(ID):
        ID = create_random_number(ID_LENGTH)
    return ID


def get_patient_info(patient_id:str)->dict:
    """데이터베이스에 저장되어있는 환자의 정보를 가져오는 함수 

    :param str patient_id: 검색하고자 하는 환자의 아이디
    :returns dict: 성공시 환자 정보를 담은 dict값, 실패시 필드 네임만 들어있는 빈 dict
    """
    field_names = PATINET_INFO_FIELD_NAMES
    error = {}
    for field_name in field_names:
        error[field_name] = ""
    with open(PATIENT_INFO_CSV_PATH, 'r', encoding='utf-8') as fd:
        patients_csv = csv.DictReader(fd)
        for patient in patients_csv:
            if patient['id'] == patient_id:
                return patient
    return error


def get_medicine_info(patient_id:str)->dict:
    """데이터베이스에 저장되어있는 환자의 약 정보를 가져오는 함수 

    :param str patient_id: 검색하고자 하는 환자의 아이디
    :returns dict: 성공시 약 정보를 담은 dict값, 실패시 필드 네임만 들어있는 빈 dict
    """
    field_names = MEDICINE_INFO_FIELD_NAMES
    error = {}
    for field_name in field_names:
        error[field_name] = ""
    with open(MEDICINE_INFO_CSV_PATH, 'r', encoding='utf-8') as fd:
        csv_dict_fd = csv.DictReader(fd)
        for medicine_info in csv_dict_fd:
            if medicine_info['id'] == patient_id:
                return medicine_info
    return error


def has_patient_id(patient_id:str)->bool:
    """데이터베이스에 환자의 정보가 있는 지 확인하는 함수

    :param str patient_id: 검색하고자 하는 환자의 아이디
    :returns bool: bool타입의 검색 결과
    """
    if get_patient_info(patient_id)['id'] == '':
        return False
    return True


def save_patient_info(patient_id:str, patient_info:dict)->bool:
    """새로운 환자의 정보를 데이터베이스에 저장

    :param str patient_id: 저장하고자 하는 환자의 아이디
    :param dict patient_info: 환자 정보
    :returns: bool 타입의 실행 결과
    """
    try:
        field_names = PATINET_INFO_FIELD_NAMES
        if has_patient_id(patient_id):
            logger.log.error("[db/database.py:save_patient_info][E] " + \
                "patient_id({}) already exists".format(patient_id))
            return False
        with open(PATIENT_INFO_CSV_PATH, 'a') as fd:
            csv_dict_fd = csv.DictWriter(fd, fieldnames=field_names)
            csv_dict_fd.writerow(patient_info)
    except Exception as e:
        logger.log.error("[db/database.py:save_patient_info][E] " + \
            "{}".format(e))
        return False
    else:
        return True


def save_medicine_info(patient_id:str, medicine_info:dict)->bool:
    """새로운 환자의 약 정보를 데이터베이스에 저장 
    필드값은 ID, medicine1, medicine2, medicine3이다.

    :param str patient_id: 저장하고자 하는 환자의 아이디
    :param dict medicine_info: 환자의 약 정보
    :returns bool: bool 타입의 실행 결과
    """
    try:
        field_names = MEDICINE_INFO_FIELD_NAMES
        if get_medicine_info(patient_id)['id'] == '':
            logger.log.error("[db/database.py:save_medicine_info][E] " + \
                "patient_id({}) already exists".format(patient_id))
            return False
        with open(MEDICINE_INFO_CSV_PATH, 'a') as fd:
            csv_dict_fd = csv.DictWriter(fd, fieldnames=field_names)
            csv_dict_fd.writerow(medicine_info)
    except Exception as e:
        logger.log.error("[db/database.py:save_medicine_info][E] " + \
            "{}".format(e))
        return False
    else:
        return True


def delete_patient_info(patient_id:str)->bool:
    """데이터베이스에서 환자 정보 삭제

    :param str patient_id: 삭제하고자 하는 환자의 아이디
    :returns: bool타입의 함수 실행 결과
    """
    try:
        field_names = PATINET_INFO_FIELD_NAMES
        if has_patient_id(patient_id) == False:
            return True
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
    except Exception as e:
        logger.log.error("[db/database.py:delete_patient_info][E] " + \
            "{}".format(e))
        return False       



def delete_medicine_info(patient_id:str)->bool:
    """데이터베이스에서 환자 약 정보 삭제

    :param str patient_id: 삭제하고자 하는 환자의 아이디
    :returns: bool타입의 함수 실행 결과
    """
    try:
        field_names = MEDICINE_INFO_FIELD_NAMES
        if get_medicine_info(patient_id)['id'] == '':
            return True
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
    except Exception as e:
        logger.log.error("[db/database.py:delete_medicine_info][E] " + \
            "{}".format(e))
        return False
