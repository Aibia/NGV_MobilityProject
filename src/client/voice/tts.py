#-*- coding:utf-8 -*-
import os
import urllib
from aiy.board import Board
import aiy.voice.tts
from client import config, logger
from client.voice import utils

CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SERVER_X_NCP_APIGW_API_KEY
LANGUAGE = config.LANGUAGE
VOICE_DIR_PATH = os.path.join(config.VOICE_DIR_PATH, 'voices')
TTS_FILE_NAME_LENGTH = config.TTS_FILE_NAME_LENGTH

def say(text:str)->bool:
    """AIY에서 제공하는 기본 TTS
    
    :param str text: 말하고자 하는 문자
    :returns: bool타입의 함수 실행 결과
    """
    try:
        with Board() as board:
            aiy.voice.tts.say(text)
    except Exception as e:
        logger.log.error("[client/voice/tts.py:say][E] {}".format(e))
        return False
    else:
        return True


def clova_tts(text:str, client_id:str=CLIENT_ID, client_secret:str=CLIENT_SECRET, lang:str=LANGUAGE)->bool:
    """네이버 클라우드 서비스를 이용한 TTS 함수 
    voices폴더 아래에 랜덤 파일이름으로 다운받은 음성(mp3)을 저장하고 음성 파일을 실행한다.
    API : https://apidocs.ncloud.com/ko/ai-naver/clova_speech_synthesis/tts/
    price : 4won/15sec 

    :param str text: 말하고자 하는 문자
    :param str client_id: 클로바 TTS 사용에 필요한 client_id (default값은 config에 저장 가능)
    :param str client_secret: 클로바 TTS 사용에 필요한 client_secret (default값은 config에 저장 가능)
    :param str lang: 사용할 언어 ( Kor, Jpn, Eng, Chn ) (default값은 config에 저장 가능)
    :returns: bool타입의 함수 실행 결과
    """
    ## TODO 
    ## Codec Problem 
    try:
        url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
        encText = urllib.parse.quote(text)
        data = "speaker=mijin&speed=0&text=" + encText
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
        request.add_header("X-NCP-APIGW-API-KEY",client_secret)
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()
        
        if(rescode == 200):
            logger.log.info("[voice/tts.py:clova_tts] Success clova_tts")
            response_body = response.read()
            if os.path.exists(VOICE_DIR_PATH) == False:
                os.mkdir(VOICE_DIR_PATH)
            file_path = os.path.join(VOICE_DIR_PATH, utils.randome_file_name(TTS_FILE_NAME_LENGTH)+".mp3")
            with open(file_path, 'wb') as fd:
                fd.write(response_body)
            logger.log.info("[voice/tts.py:clova_tts] TTS Voice File Saved to {}".format(file_path))
            return utils.play_mp3(file_path)
    except Exception as e:
        logger.log.error("[voice/tts.py:clova_tts][E] {}".format(e))
        return False
    else:
        logger.log.error("[voice/tts.py:clova_tts][E] clova_tts rescode {}".format(rescode)) 
        return False