# client.voice.stt module


### client.voice.stt.clova_stt(client_id='example', client_secret='example', lang='Kor')
네이버 클로바 클라우드 서비스를 이용한 STT 함수 voices폴더 아래에 랜덤 파일이름으로 음성(wav)이 저장된다.
API : [https://apidocs.ncloud.com/ko/ai-naver/clova_speech_recognition/stt/](https://apidocs.ncloud.com/ko/ai-naver/clova_speech_recognition/stt/)
price : 4won/15sec


* **Parameters**

    
    * **client_id** (*str*) – 클로바 STT 사용에 필요한 client_id (default값은 config에 저장 가능)


    * **client_secret** (*str*) – 클로바 STT 사용에 필요한 client_secret (default값은 config에 저장 가능)


    * **lang** (*str*) – 사용할 언어 ( Kor, Jpn, Eng, Chn ) (default값은 config에 저장 가능)



* **Returns**

    


### client.voice.stt.is_korean_chr(chr_u)
check if korean characters
see [http://www.unicode.org/reports/tr44/#GC_Values_Table](http://www.unicode.org/reports/tr44/#GC_Values_Table)
