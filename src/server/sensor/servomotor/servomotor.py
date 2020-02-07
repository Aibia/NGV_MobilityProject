import RPI.GPIO as gpio

motor_pin_info = {
     #motor_name : motor_pin_num
     "medicine1" : 14,
     "medicine2" : 15,
     "medicine3" : 16
}
 
def medicine_out(motor_name, times):
    if motor_name not in motor_pin_info.keys():
        return False
    
    gpio.setwarnings(False)
    # pin의 호출 방식 
    gpio.setmode(gpio.BOARD)
    gpio.setup(motor_pin_info[motor_name], gpio.OUT)

    p=gpio.PWM(motor_pin_info[motor_name],50)
    p.start(0)
    p.ChangeDutyCycle(12)
    time.sleep(2)

    p.ChangeDutyCycle(2.5)
    time.sleep(2) 
    gpio.cleanup()
    return True 
