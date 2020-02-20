# client.client module


### class client.client.Client()
Bases: `object`


#### is_nasa_running()
차량이 작동중인지의 여부를 확인할 수 있는 함수 
서버에 리퀘스트를 보내 정해진 gpio값의 상태가 “out”인 경우 차량이 움직이고 있다고 판단한다.


* **Returns bool**

    차량이 작동중일 경우 True를 반환한다.



#### is_web_running()
웹서버가 작동중인지의 여부를 확인할 수 있는 함수


* **Returns bool**

    웹 서버가 작동중일 경우 True를 반환한다.



#### start()
(main함수)웹서버와 얼굴인식 및 서보를 동작시킨다.


* **Returns bool**

    실행 결과



#### stop(sig, frame)
