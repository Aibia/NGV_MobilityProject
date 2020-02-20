# client.db.database module


### client.db.database.create_new_id()
config파일에 지정되어있는 ID길이에 맞는 환자 ID 생성


* **Returns str**

    문자형 환자 아이디



### client.db.database.create_random_number(length)
랜덤한 숫자(문자열)를 생성해내는 함수 입니다.


* **Parameters**

    **length** (*int*) – 랜덤 숫자의 길이를 결정 짓는 int



* **Returns str**

    문자열 타입의 랜덤 숫자



### client.db.database.create_random_string(length)
랜덤한 문자열을 생성해내는 함수 입니다.


* **Parameters**

    **length** (*int*) – 랜덤 숫자의 길이를 결정 짓는 int



* **Returns str**

    랜덤 문자열



### client.db.database.delete_medicine_info(patient_id)
데이터베이스에서 환자 약 정보 삭제


* **Parameters**

    **patient_id** (*str*) – 삭제하고자 하는 환자의 아이디



* **Returns bool**

    bool타입의 함수 실행 결과



### client.db.database.delete_patient_info(patient_id)
데이터베이스에서 환자 정보 삭제


* **Parameters**

    **patient_id** (*str*) – 삭제하고자 하는 환자의 아이디



* **Returns bool**

    bool타입의 함수 실행 결과



### client.db.database.get_medicine_info(patient_id)
데이터베이스에 저장되어있는 환자의 약 정보를 가져오는 함수


* **Parameters**

    **patient_id** (*str*) – 검색하고자 하는 환자의 아이디



* **Returns dict**

    성공시 약 정보를 담은 dict값, 실패시 필드 네임만 들어있는 빈 dict



### client.db.database.get_patient_info(patient_id)
데이터베이스에 저장되어있는 환자의 정보를 가져오는 함수


* **Parameters**

    **patient_id** (*str*) – 검색하고자 하는 환자의 아이디



* **Returns dict**

    성공시 환자 정보를 담은 dict값, 실패시 필드 네임만 들어있는 빈 dict



### client.db.database.has_patient_id(patient_id)
데이터베이스에 환자의 정보가 있는 지 확인하는 함수


* **Parameters**

    **patient_id** (*str*) – 검색하고자 하는 환자의 아이디



* **Returns bool**

    bool타입의 검색 결과



### client.db.database.save_medicine_info(patient_id, medicine_info)
새로운 환자의 약 정보를 데이터베이스에 저장 
필드값은 ID, medicine1, medicine2, medicine3이다.


* **Parameters**

    
    * **patient_id** (*str*) – 저장하고자 하는 환자의 아이디


    * **medicine_info** (*dict*) – 환자의 약 정보



* **Returns bool**

    bool 타입의 실행 결과



### client.db.database.save_patient_info(patient_id, patient_info)
새로운 환자의 정보를 데이터베이스에 저장


* **Parameters**

    
    * **patient_id** (*str*) – 저장하고자 하는 환자의 아이디


    * **patient_info** (*dict*) – 환자 정보



* **Returns bool**

    bool 타입의 실행 결과
