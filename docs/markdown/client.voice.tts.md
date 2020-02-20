# client.voice.tts module


### client.voice.tts.clova_tts(text, client_id='example', client_secret='example', lang='Kor')
네이버 클라우드 서비스를 이용한 TTS 함수 
voices폴더 아래에 랜덤 파일이름으로 다운받은 음성(mp3)을 저장하고 음성 파일을 실행한다.
API : [https://apidocs.ncloud.com/ko/ai-naver/clova_speech_synthesis/tts/](https://apidocs.ncloud.com/ko/ai-naver/clova_speech_synthesis/tts/)
price : 4won/15sec


* **Parameters**

    
    * **text** (*str*) – 말하고자 하는 문자


    * **client_id** (*str*) – 클로바 TTS 사용에 필요한 client_id (default값은 config에 저장 가능)


    * **client_secret** (*str*) – 클로바 TTS 사용에 필요한 client_secret (default값은 config에 저장 가능)


    * **lang** (*str*) – 사용할 언어 ( Kor, Jpn, Eng, Chn ) (default값은 config에 저장 가능)



* **Returns**

    bool타입의 함수 실행 결과



### client.voice.tts.say(text)
AIY에서 제공하는 기본 TTS


* **Parameters**

    **text** (*str*) – 말하고자 하는 문자



* **Returns**

    bool타입의 함수 실행 결과
