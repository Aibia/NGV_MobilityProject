import os

## DIR PATH
ROOT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
DB_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'db')
LOG_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'log')
SENSOR_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'sensor')
VISION_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'vision')
VOICE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'voice')


## SERVER CONFIG
SERVER_IP_ADDR = '192.168.0.10'
SERVER_PORT = 4000
MOTOR_STOP_PIN_NUM = 15

## DB CONFIG
PATIENT_INFO_CSV_PATH = os.path.join(DB_DIR_PATH, 'patients.csv')
MEDICINE_INFO_CSV_PATH = os.path.join(DB_DIR_PATH, 'medicine_info.csv')

## SENSOR CONFIG
SERVO_MIN_ANGLE = -90
SERVO_MAX_ANGLE = 90

## VISION CONFIG


## VOICE CONFIG