#-*- coding:utf-8 -*-
import requests
import json
from client import config, logger


SERVER_IP_ADDR = config.SERVER_IP_ADDR
SERVER_PORT = config.SERVER_PORT
MOTOR_STOP_PIN_NUM = config.MOTOR_STOP_PIN_NUM


def is_webserver_up()->bool:
    """jsonrpc 서버와의 연결을 확인하는 함수

    :returns bool: 서버와 연결이 되어있으면 True 아님 False를 반환한다.
    """
    url = "http://"+SERVER_IP_ADDR+":"+str(SERVER_PORT)+"/jsonrpc"
    req = requests.head(url)
    return req.status_code == 200


def gpio_pin_change_out()->bool:
    """모터를 제어하는 서버측 GPIO 핀을 OUT으로 바꿈 
    설정은 config파일에서 할 수 있음 [SERVER_IP_ADDR, SERVER_PORT, MOTOR_STOP_PIN_NUM]

    :returns bool: 서버에 요청 결과 
    """
    url = "http://"+SERVER_IP_ADDR+":"+str(SERVER_PORT)+"/jsonrpc"

    # Example echo method
    payload = {
        "method": "gpio_pin_change",
        "params": [MOTOR_STOP_PIN_NUM, "OUT"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    result = requests.post(url, json=payload).json()
    if "error" in result.keys():
        logger.log.error("[sensor/request.py:gpio_pin_change_out] {}".format(result["error"]))
        return False
    return result["result"]


def gpio_pin_change_in()->bool:
    """모터를 제어하는 서버측 GPIO 핀을 IN으로 바꿈 
    설정은 config파일에서 할 수 있음 [SERVER_IP_ADDR, SERVER_PORT, MOTOR_STOP_PIN_NUM]

    :returns bool: 서버에 요청 결과 
    """
    url = "http://"+SERVER_IP_ADDR+":"+str(SERVER_PORT)+"/jsonrpc"

    # Example echo method
    payload = {
        "method": "gpio_pin_change",
        "params": [MOTOR_STOP_PIN_NUM, "IN"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    result = requests.post(url, json=payload).json()
    if "error" in result.keys():
        logger.log.error("[sensor/request.py:gpio_pin_change_in] {}".format(result["error"]))
        return False
    return result["result"]


def get_gpio_pin_function()->str:
    """모터를 제어하는 서버측 GPIO 핀의 설정 값을 갖고옴

    :returns str: 서버에 요청 결과 (out, in, 빈스트링 3가지)
    """
    url = "http://"+SERVER_IP_ADDR+":"+str(SERVER_PORT)+"/jsonrpc"

    # Example echo method
    payload = {
        "method": "get_gpio_pin_function",
        "params": [MOTOR_STOP_PIN_NUM],
        "jsonrpc": "2.0",
        "id": 0,
    }
    result = requests.post(url, json=payload).json()
    if "error" in result.keys():
        logger.log.error("[sensor/request.py:get_gpio_pin_function] {}".format(result["error"]))
        return ""
    return result["result"]


