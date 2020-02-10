import os
import numpy as np
from datetime import date
import string
import random
from client.db import database

ID_LENGTH = 10
STRING_POOL = string.ascii_lowercase
random.seed(0)
CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
YML_DIR_PATH = os.path.join(CURRENT_DIR_PATH, 'ymls')
PATIENT_DATABASE_CSV_PATH = ""

def reshape(array, width):
    assert len(array) % width == 0
    height = len(array) // width
    return [array[i * width:(i+1) * width] for i in range(height)]


def get_latest_yml_path():
    dates = os.listdir(YML_DIR_PATH)
    dates.sort()
    if len(dates) > 0:
        return os.path.join(YML_DIR_PATH, "{}.yml".format(dates[-1]))
    else:
        return ""

def create_random_string():
    RANDOM_STRING = ""
    for i in range(ID_LENGTH):
        RANDOM_STRING += random.choice(STRING_POOL)
    return RANDOM_STRING

def create_new_id():
    ID = create_random_string()
    while database.has_patient_id(ID):
        ID = create_random_string()
    return ID



