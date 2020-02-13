from aiy.pins import PIN_A, PIN_B, PIN_C
from gpiozero import AngularServo
from client import config
import time


SERVO_MIN_ANGLE = config.SERVO_MIN_ANGLE
SERVO_MAX_ANGLE = config.SERVO_MAX_ANGLE
MIN_PULSE_WIDTH = config.MIN_PULSE_WIDTH
MAX_PULSE_WIDTH = config.MAX_PULSE_WIDTH

motor_pin_info = {
    #motor_name : motor_pin_num
    "medicine1" : AngularServo(PIN_A, min_angle=SERVO_MIN_ANGLE, \
        max_angle=SERVO_MAX_ANGLE, min_pulse_width=MIN_PULSE_WIDTH, max_pulse_width=MAX_PULSE_WIDTH),
    "medicine2" : AngularServo(PIN_B, min_angle=SERVO_MIN_ANGLE, \
        max_angle=SERVO_MAX_ANGLE, min_pulse_width=MIN_PULSE_WIDTH, max_pulse_width=MAX_PULSE_WIDTH),
    "medicine3" : AngularServo(PIN_C, min_angle=SERVO_MAX_ANGLE, \
        max_angle=SERVO_MIN_ANGLE, min_pulse_width=MIN_PULSE_WIDTH, max_pulse_width=MAX_PULSE_WIDTH)
}

def medicine_out(medicine_info):
    try:
        for motor_name in medicine_info.keys():
            if motor_name == "id":
                continue
            control_servo_motor(motor_name, int(medicine_info[motor_name]))           
    except Exception as e:
        return False 
    else:
        return True 


def control_servo_motor(motor_name, times):
    if motor_name not in motor_pin_info.keys():
        return False

    servo = motor_pin_info[motor_name]
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
    return True
