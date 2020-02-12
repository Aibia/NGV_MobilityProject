import sys
import requests
import json
import urllib.request
from aiy.cloudspeech import CloudSpeechClient
from aiy.board import Board
from client import config
from client.voice import utils



client_id = config.CLIENT_ID
client_secret = config.CLIENT_SERVER_X_NCP_APIGW_API_KEY
LANGUAGE = config.LANGUAGE
STT_FILE_NAME_LENGTH = config.STT_FILE_NAME_LENGTH

# clova stt
def clova_stt(client_id=client_id, client_secret=client_secret, lang=LANGUAGE):
    #
    # API : https://apidocs.ncloud.com/ko/ai-naver/clova_speech_recognition/stt/
    # price : 4won/15sec 
    #
    url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
    data = open(utils.voice_recoder(utils.randome_file_name(STT_FILE_NAME_LENGTH)), 'rb')
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
            return response_json["text"]
        else:
            return "Error : No Text Key"
    else:
        return "Error : {}".format(response.text)
    
