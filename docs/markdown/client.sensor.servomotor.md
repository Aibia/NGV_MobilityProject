# client.sensor.servomotor module


### client.sensor.servomotor.control_servo_motor(medicine_name, times)
약의 이름과 횟수에 맞게 서보모터를 작동시켜 약을 배출한다.


* **Parameters**

    
    * **medicine_name** (*str*) – 약의 이름


    * **times** (*int*) – 약 배출 횟수



* **Returns bool**

    bool형의 함수 실행 결과



### client.sensor.servomotor.medicine_out(medicine_info)
약 정보(medicine_info)에 맞는 약을 배출


* **Parameters**

    **medicine_info** (*dict*) – 약이름과 섭취해야하는 약의 개수가 담겨있다.



* **Returns bool**

    bool형의 함수 실행결과
