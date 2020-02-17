import sys
import requests
import json
import urllib.request
from aiy.cloudspeech import CloudSpeechClient
from aiy.board import Board
from client import config, logger
from client.voice import utils


CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SERVER_X_NCP_APIGW_API_KEY
LANGUAGE = config.LANGUAGE
STT_FILE_NAME_LENGTH = config.STT_FILE_NAME_LENGTH


def clova_stt(client_id:str=CLIENT_ID, client_secret:str=CLIENT_SECRET, lang:str=LANGUAGE)->str:
    """네이버 클로바 클라우드 서비스를 이용한 STT 함수 voices폴더 아래에 랜덤 파일이름으로 음성(wav)이 저장된다.
    API : https://apidocs.ncloud.com/ko/ai-naver/clova_speech_recognition/stt/
    price : 4won/15sec

    :param str client_id: 클로바 STT 사용에 필요한 client_id (default값은 config에 저장 가능)
    :param str client_secret: 클로바 STT 사용에 필요한 client_secret (default값은 config에 저장 가능)
    :param str lang: 사용할 언어 ( Kor, Jpn, Eng, Chn ) (default값은 config에 저장 가능)
    :returns: 
    """
    try:
        url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
        data = open(utils.voice_recoder(utils.randome_file_name(STT_FILE_NAME_LENGTH)+".wav"), 'rb')
        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
            "Content-Type": "application/octet-stream"
        }
        response = requests.post(url,  data=data, headers=headers)
        rescode = response.status_code
        if(rescode == 200):
            response_json = json.loads(response.text)
            if "text" in response_json.keys():
                logger.log.info("[voice/stt.py:clova_stt] STT result {}".format(response_json["text"]))
                return response_json["text"]
            else:
                logger.log.error("[voice/stt.py:clova_stt][E] No Text Key")
                return ""
    except Exception as e:
        logger.log.error("[voice/stt.py:clova_stt][E] {}".format(e))
        return ""
    else:
        logger.log.error("[voice/stt.py:clova_stt][E] clova_stt rescode {}".format(rescode)) 
        return ""
    
