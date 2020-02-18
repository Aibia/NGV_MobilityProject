#-*- coding:utf-8 -*-
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import RPi.GPIO as GPIO
from server import config, logger

@dispatcher.add_method
def gpio_pin_change(pin_num, pin_opt):
    try:
        GPIO.setmode(GPIO.BOARD)
        if pin_opt == "OUT":
            GPIO.setup(int(pin_num), GPIO.OUT)
        elif pin_opt == "IN":
            GPIO.setup(int(pin_num), GPIO.IN)
        else:
            return False
    except Exception as e:
        return False
    else:
        return True


@dispatcher.add_method
def get_gpio_pin_function(pin_num):
    try:
        GPIO.setmode(GPIO.BOARD)
        gpio_funcition = GPIO.gpio_function(pin_num)
        if gpio_funcition == GPIO.OUT:
            return "out"
        elif gpio_funcition == GPIO.IN:
            return "in"
        else:
            return "unknown"
    except Exception as e:
        return "unknown"


@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


def run_sensor_server():
    logger.log.info("[sensor_server.py:run_sensor_server] Start server {}:{} ...".format(config.SERVER_IP_ADDR, config.SERVER_PORT))
    run_simple(config.SERVER_IP_ADDR, config.SERVER_PORT, application)


def stop_sensor_server():
    logger.log.info("[sensor_server.py:run_sensor_server] Stop server {}:{} ...".format(config.SERVER_IP_ADDR, config.SERVER_PORT))