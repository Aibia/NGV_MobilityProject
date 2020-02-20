# client.vision.register module


### client.vision.register.train(patient_id, data_path)
환자의 얼굴을 인식시키기 위해 아이디별로 이미지를 학습시킨다.


* **Parameters**

    
    * **patient_id** (*str*) – 학습시킬 환자의 아이디


    * **data_path** (*str*) – 학습시킬 환자의 이미지가 저장되어있는 경로



* **Returns bool**

    주어진 데이터에서 찾아진 얼굴 데이터와 라벨값을 이용하여 train_recognizer함수를 통해 학습시킨 결과 값



### client.vision.register.train_recognizer(datasets, recognizer_path='/Users/nuguni/Downloads/project/src/client/vision/ymls/2020-02-21.yml', old_recognizer=False)
데이터를 바탕으로 얼굴 정보를 학습시킨다. 
학습된 YML파일은 recognizer_path에 저장되며 OLD_RECOGNIZER에 따라 이전 파일에 추가할 수 있다.


* **Parameters**

    
    * **datasets** (*dict*) – 학습시킬 데이터셋


    * **recognizer_path** (*str*) – 학습된 YML파일을 저장할 경로


    * **old_recognizer** (*bool*) – 이전파일에 추가적으로 학습시킬때 사용되는 flag이값이 참일 경우 recognizer_path는 자동으로 가장 최근의 YML파일의 경로로 바뀐다.



* **Returns bool**

    얼굴 데이터와 라벨을 이용하여 이미지를 학습시킨 결과
