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


@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


def run_sensor_server():
    logger.log.info("Start server {}:{} ...".format(config.SERVER_IP_ADDR, config.SERVER_PORT))
    run_simple(config.SERVER_IP_ADDR, config.SERVER_PORT, application)


def stop_sensor_server():
    logger.log.info("Stop server {}:{} ...".format(config.SERVER_IP_ADDR, config.SERVER_PORT))