import requests
import json

PORT = 4000
SERVER_PIN_NUM=17

def gpio_pin_change_out(server_ip):
    url = "http://"+server_ip+":"+PORT+"/jsonrpc"

    # Example echo method
    payload = {
        "method": "gpio_pin_change",
        "params": [SERVER_PIN_NUM, "OUT"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    return requests.post(url, json=payload).json()

def gpio_pin_change_in(server_ip):
    url = "http://"+server_ip+":"+PORT+"/jsonrpc"

    # Example echo method
    payload = {
        "method": "gpio_pin_change",
        "params": [SERVER_PIN_NUM, "IN"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    return requests.post(url, json=payload).json()

def medicine_out(server_ip, medicine_info):
    url = "http://"+server_ip+":"+PORT+"/jsonrpc"
    
    payload = {
        "method" : "medicine_out",
        "params" : [medicine_info],
        "jsonrpc" : "2.0",
        "id" : 0,
    }
    return requests.post(url, json=payload).json() 

