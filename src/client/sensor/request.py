import requests
import json

PORT = 4000
SERVER_PIN_NUM=15

def gpio_pin_change_out(server_ip):
    url = "http://"+server_ip+":"+str(PORT)+"/jsonrpc"

    # Example echo method
    payload = {
        "method": "gpio_pin_change",
        "params": [SERVER_PIN_NUM, "OUT"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    return requests.post(url, json=payload).json()

def gpio_pin_change_in(server_ip):
    url = "http://"+server_ip+":"+str(PORT)+"/jsonrpc"

    # Example echo method
    payload = {
        "method": "gpio_pin_change",
        "params": [SERVER_PIN_NUM, "IN"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    return requests.post(url, json=payload).json()


