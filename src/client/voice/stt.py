import sys
import requests
from aiy.cloudspeech import CloudSpeechClient
from aiy.board import Board

# clova stt
def clova_stt(lang="Kor", client_id, client_secret, voice_file_path):
    #
    # API : https://apidocs.ncloud.com/ko/ai-naver/clova_speech_recognition/stt/
    # price : 4won/15sec 
    #
    url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
    data = open(voice_file_path, 'rb')
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/octet-stream"
    }
    response = requests.post(url,  data=data, headers=headers)
    rescode = response.status_code
    if(rescode == 200):
        return response.text
    else:
        return "Error : {}".format(response.text)

# google stt
def google_stt(language_code = 'en-US' , hint_phrases=('yes', 'no')):
    #
    # make sure that assistant.json file is in the correct folder
    # https://aiyprojects.readthedocs.io/en/latest/aiy.cloudspeech.html
    # The Google Cloud Speech-to-Text service is a cloud-based service. If you use it for less than 60 minutes a month, it’s free. Beyond that, the cost is $0.006 for every 15 seconds. Don’t worry: you’ll get a reminder if you go over your free limit.
    #
    client = CloudSpeechClient()
    with Board() as board:
        while True:
            text = client.recognize(language_code=language_code, hint_phrases=hint_phrases)
            if text is None:
                return ""
            else:
                return text
    
