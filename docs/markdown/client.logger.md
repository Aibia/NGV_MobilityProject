# client.logger module


### class client.logger.Logger()
Bases: `object`

Logger클래스 
로깅을 하기 위한 클래스

콘솔과 파일 동시에 로깅한다.


#### debug(text)
디버깅을 위한 로깅


* **Parameters**

    **text** (*str*) – 로깅할 문자



* **Returns**

    파일에 로깅



#### error(text)
에러를 로깅


* **Parameters**

    **text** (*str*) – 로깅할 문자



* **Returns**

    파일에 로깅



#### info(text)
기본 로깅 함수


* **Parameters**

    **text** (*str*) – 로깅할 문자



* **Returns**

    파일에 로깅



#### instance( = <client.logger.Logger object>)

#### warning(text)
경고하기 위한 로깅


* **Parameters**

    **text** (*str*) – 로깅할 문자



* **Returns**

    파일에 로깅
