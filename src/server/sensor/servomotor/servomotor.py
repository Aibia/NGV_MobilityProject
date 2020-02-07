import RPI.GPIO as gpio

motor_pin_nums = [14,15,16]

def medicine_out(motor_pin_num, times):
    if motor_pin_num not in motor_pin_nums:
        return False
    gpio.setup(motor_pin_num, gpio.OUT)
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(pin2, gpio.OUT)

    p=gpio.PWM(pin2,50)
    p.start(0)
    p.ChangeDutyCycle(12)
    time.sleep(2)

    p.ChangeDutyCycle(2.5)
    time.sleep(2) 
    return True 
