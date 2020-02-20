# client.sensor.request module


### client.sensor.request.get_gpio_pin_function()
모터를 제어하는 서버측 GPIO 핀의 설정 값을 갖고옴


* **Returns str**

    서버에 요청 결과 (out, in, 빈스트링 3가지)



### client.sensor.request.gpio_pin_change_in()
모터를 제어하는 서버측 GPIO 핀을 IN으로 바꿈 
설정은 config파일에서 할 수 있음 [SERVER_IP_ADDR, SERVER_PORT, MOTOR_STOP_PIN_NUM]


* **Returns bool**

    서버에 요청 결과



### client.sensor.request.gpio_pin_change_out()
모터를 제어하는 서버측 GPIO 핀을 OUT으로 바꿈 
설정은 config파일에서 할 수 있음 [SERVER_IP_ADDR, SERVER_PORT, MOTOR_STOP_PIN_NUM]


* **Returns bool**

    서버에 요청 결과



### client.sensor.request.is_webserver_up()
jsonrpc 서버와의 연결을 확인하는 함수


* **Returns bool**

    서버와 연결이 되어있으면 True 아님 False를 반환한다.
