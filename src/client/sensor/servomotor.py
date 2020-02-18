from aiy.pins import PIN_A, PIN_B, PIN_C
from gpiozero import AngularServo
from client import config, logger
import time


SERVO_MIN_ANGLE = config.SERVO_MIN_ANGLE
SERVO_MAX_ANGLE = config.SERVO_MAX_ANGLE
MIN_PULSE_WIDTH = config.MIN_PULSE_WIDTH
MAX_PULSE_WIDTH = config.MAX_PULSE_WIDTH

def medicine_out(medicine_info:dict)->bool:
    """약 정보(medicine_info)에 맞는 약을 배출 
    
    :param dict medicine_info: 약이름과 섭취해야하는 약의 개수가 담겨있다. 
    :returns bool: bool형의 함수 실행결과
    """
    try:
        for motor_name in medicine_info.keys():
            if motor_name == "id":
                continue
            control_servo_motor(motor_name, int(medicine_info[motor_name]))           
    except Exception as e:
        logger.log.error("[sensor/servomotor.py:medicine_out][E] {}".format(e))
        return False 
    else:
        return True 


def control_servo_motor(medicine_name:str, times:int)->bool:
    """약의 이름과 횟수에 맞게 서보모터를 작동시켜 약을 배출한다.

    :param str medicine_name: 약의 이름
    :param int times: 약 배출 횟수
    :returns bool: bool형의 함수 실행 결과 
    """
    motor_pin_info = {
        #motor_name : motor_pin_num
        "medicine1" : AngularServo(PIN_A, min_angle=SERVO_MIN_ANGLE, \
            max_angle=SERVO_MAX_ANGLE, min_pulse_width=MIN_PULSE_WIDTH, max_pulse_width=MAX_PULSE_WIDTH),
        "medicine2" : AngularServo(PIN_B, min_angle=SERVO_MIN_ANGLE, \
            max_angle=SERVO_MAX_ANGLE, min_pulse_width=MIN_PULSE_WIDTH, max_pulse_width=MAX_PULSE_WIDTH),
        "medicine3" : AngularServo(PIN_C, min_angle=SERVO_MAX_ANGLE, \
            max_angle=SERVO_MIN_ANGLE, min_pulse_width=MIN_PULSE_WIDTH, max_pulse_width=MAX_PULSE_WIDTH)
    }
    
    if medicine_name not in motor_pin_info.keys():
        return False

    try:
        servo = motor_pin_info[medicine_name]
        for _ in range(times):
            if servo.angle == servo.min_angle:
                servo.max()
                time.sleep(2)
                servo.min()
                time.sleep(2)
            else:
                servo.min()
                time.sleep(2)
                servo.max()
                time.sleep(2)
    except Exception as e:
        logger.log.error("[sensor/servomotor.py:control_servo_motor][E] {}".format(e))
        return False
    return True
