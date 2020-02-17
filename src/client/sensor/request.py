import requests
import json
from client import config


SERVER_IP_ADDR = config.SERVER_IP_ADDR
SERVER_PORT = config.SERVER_PORT
MOTOR_STOP_PIN_NUM = config.MOTOR_STOP_PIN_NUM


def gpio_pin_change_out()->dict:
    """모터를 멈추기 위해 서버측 GPIO 핀을 OUT으로 바꿈 
    설정은 config파일에서 할 수 있음 [SERVER_IP_ADDR, SERVER_PORT, MOTOR_STOP_PIN_NUM]

    :returns: 서버에 요청 결과 
    """
    url = "http://"+SERVER_IP_ADDR+":"+str(SERVER_PORT)+"/jsonrpc"

    # Example echo method
    payload = {
        "method": "gpio_pin_change",
        "params": [MOTOR_STOP_PIN_NUM, "OUT"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    return requests.post(url, json=payload).json()


def gpio_pin_change_in()->dict:
    """모터를 다시 작동시키기 위해 서버측 GPIO 핀을 IN으로 바꿈 
    설정은 config파일에서 할 수 있음 [SERVER_IP_ADDR, SERVER_PORT, MOTOR_STOP_PIN_NUM]

    :returns: 서버에 요청 결과 
    """
    url = "http://"+SERVER_IP_ADDR+":"+str(SERVER_PORT)+"/jsonrpc"

    # Example echo method
    payload = {
        "method": "gpio_pin_change",
        "params": [MOTOR_STOP_PIN_NUM, "IN"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    return requests.post(url, json=payload).json()


