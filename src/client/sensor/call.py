import requests
import json

PORT = 4000

def gpio_pin_change_out(server_ip):
    url = "http://"+server_ip+":"+PORT+"/jsonrpc"

    # Example echo method
    payload = {
        "method": "gpio_pin_change",
        "params": ["17", "OUT"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    return requests.post(url, json=payload).json()

def gpio_pin_change_in(server_ip):
    url = "http://"+server_ip+":"+PORT+"/jsonrpc"

    # Example echo method
    payload = {
        "method": "gpio_pin_change",
        "params": ["17", "IN"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    return requests.post(url, json=payload).json()

def move_servo_motor(server_ip, motor_info):
    url = "http://"+server_ip+":"+PORT+"/jsonrpc"
    
    payload = {
        "method" : "move_servo_motor",
        "params" : [motor_info],
        "jsonrpc" : "2.0",
        "id" : 0,
    }
    return requests.post(url, json=payload).json() 

