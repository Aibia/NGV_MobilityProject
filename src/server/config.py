import os

## DIR PATH
ROOT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
LOG_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'log')
SENSOR_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'sensor')


## DRIVE CONFIG
MOTOR_STOP_PIN_NUM = 15


## SERVER CONFIG
SERVER_IP_ADDR = '127.0.0.1'
SERVER_PORT = 4000