from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
from servomotor import servomotor as sm
import RPi.GPIO as gpio


@dispatcher.add_method
def gpio_pin_change(pin_num, pin_opt): 
    try:
        if pin_opt == "OUT":
            gpio.setup(int(pin_num), gpio.OUT)
        elif pin_opt == "IN":
            gpio.setup(int(pin_num), gpio.IN)
        else:
            return False
    except Exception as e:
        return False 
    else:
        return True 


@dispatcher.add_method
def medicine_out(medicine_info): 
    try:
        for motor_pin_num in medicine_info.keys():
            if motor_pin_num == "id":
                continue
            sm.medicine_out(motor_pin_num, medicine_info[motor_pin_num])           
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


if __name__ == '__main__':
    run_simple('localhost', 4000, application)
