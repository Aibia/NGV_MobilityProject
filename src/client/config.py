import os

## DIR PATH
ROOT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
DB_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'db')
LOG_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'log')
SENSOR_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'sensor')
VISION_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'vision')
VOICE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'voice')
HTML_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'html')

## SERVER CONFIG
SERVER_IP_ADDR = '192.168.0.10'
SERVER_PORT = 4000
MOTOR_STOP_PIN_NUM = 15

## HTML CONFIG
APP_PATH = os.path.join(HTML_DIR_PATH, 'app.py')
HOST_IP_ADDR = '192.168.255.30'
TEMP_IMAGE_FILE_NAME_LENGTH = 20

## DB CONFIG
ID_LENGTH = 10
PATIENT_INFO_CSV_PATH = os.path.join(DB_DIR_PATH, 'patients.csv')
MEDICINE_INFO_CSV_PATH = os.path.join(DB_DIR_PATH, 'medicine_info.csv')


## SENSOR CONFIG
SERVO_MIN_ANGLE = 0
SERVO_MAX_ANGLE = 180
MIN_PULSE_WIDTH = 0.0006
MAX_PULSE_WIDTH = 0.0024

## VISION CONFIG
DISPLAY_ON = False
DISPLAY_COLOR_ON = False

## VOICE CONFIG
CLOUD_TTS_ON = False
CLOUD_STT_ON = False
LANGUAGE = "Kor" ## 언어 코드 ( Kor, Jpn, Eng, Chn )
APPLICATION_NAME = "ngv"
CLIENT_ID = "7q1xxkbepv"
CLIENT_SERVER_X_NCP_APIGW_API_KEY = "MrJYR9B5dapyW2iAmAgo5NAfvIEvtoG8a6vwFSTv"
STT_FILE_NAME_LENGTH = 5
TTS_FILE_NAME_LENGTH = 5