import requests
import json
from client import config


SERVER_IP_ADDR = config.SERVER_IP_ADDR
SERVER_PORT = config.SERVER_PORT
MOTOR_STOP_PIN_NUM = config.MOTOR_STOP_PIN_NUM


def gpio_pin_change_out():
    url = "http://"+SERVER_IP_ADDR+":"+str(SERVER_PORT)+"/jsonrpc"

    # Example echo method
    payload = {
        "method": "gpio_pin_change",
        "params": [MOTOR_STOP_PIN_NUM, "OUT"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    return requests.post(url, json=payload).json()


def gpio_pin_change_in():
    url = "http://"+SERVER_IP_ADDR+":"+str(SERVER_PORT)+"/jsonrpc"

    # Example echo method
    payload = {
        "method": "gpio_pin_change",
        "params": [MOTOR_STOP_PIN_NUM, "IN"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    return requests.post(url, json=payload).json()


