# client.vision.cascade.haar module


### client.vision.cascade.haar.find_face()
실시간으로 얼굴을 찾아서 반환함


* **Returns numpy.ndarray**

    찾아진 그레이 스케일 된 얼굴 이미지 데이터



### client.vision.cascade.haar.get_gray_face(frame)
그레이 스케일된 이미지에서 얼굴부분을 크롭해 반환한다.


* **Parameters**

    **frame** (*numpy.ndarray*) – 얼굴을 찾고자 하는 그레이스케일된 이미지 파일



* **Returns numpy.ndarray**

    찾아진 얼굴
