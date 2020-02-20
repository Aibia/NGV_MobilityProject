# client.voice.utils module


### client.voice.utils.play_mp3(file_path)
mp3형식의 오디오 파일을 mpg123를 이용해 실행한다.


* **Parameters**

    **file_path** (*str*) – 오디오 파일의 경로



* **Returns**

    bool타입의 함수 실행 결과



### client.voice.utils.randome_file_name(length)
랜덤 문자열인 파일 이름을 생성한다.


* **Parameters**

    **length** (*int*) – 파일 이름 길이



* **Returns**

    랜덤 문자열 파일 이름



### client.voice.utils.voice_recoder(file_name)
voices 폴더에 file_name으로 음성 파일을 녹음해 저장한다. 버튼을 누르면 음성 녹음이 종료된다.


* **Parameters**

    **file_name** (*str*) – 음성 파일을 저장할 파일 이름



* **Returns**

    음성 파일의 절대 경로, 실행 실패시 빈 문자열을 리턴한다.
