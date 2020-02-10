from aiy.pins import PIN_A, PIN_B, PIN_C
from gpiozero import AngularServo
from .. import config


SERVO_MIN_ANGLE = config.SERVO_MIN_ANGLE
SERVO_MAX_ANGLE = config.SERVO_MAX_ANGLE


motor_pin_info = {
     #motor_name : motor_pin_num
     "medicine1" : AngularServo(PIN_A, min_angle=SERVO_MIN_ANGLE, max_angle=SERVO_MAX_ANGLE),
     "medicine2" : AngularServo(PIN_B, min_angle=SERVO_MIN_ANGLE, max_angle=SERVO_MAX_ANGLE),
     "medicine3" : AngularServo(PIN_C, min_angle=SERVO_MIN_ANGLE, max_angle=SERVO_MAX_ANGLE)
}


def medicine_out(medicine_info):
    try:
        for motor_name in medicine_info.keys():
            if motor_name == "id":
                continue
            control_servo_motor(motor_name, medicine_info[motor_name])           
    except Exception as e:
        return False 
    else:
        return True 


def control_servo_motor(motor_name, times):
    if motor_name not in motor_pin_info.keys():
        return False
    
    servo = motor_pin_info[motor_name]
    servo.max()
    time.sleep(2)
    servo.min()
    time.sleep(2)
    return True
