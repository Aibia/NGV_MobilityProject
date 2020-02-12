import os
import urllib
from aiy.board import Board
import aiy.voice.tts
from client import config, logger
from client.voice import utils

client_id = config.CLIENT_ID
client_secret = config.CLIENT_SERVER_X_NCP_APIGW_API_KEY
VOICE_DIR_PATH = os.path.join(config.VOICE_DIR_PATH, 'voices')
TTS_FILE_NAME_LENGTH = config.TTS_FILE_NAME_LENGTH

def say(text):
    """
    text : 
    description : 
    """
    with Board() as board:
        aiy.voice.tts.say(text)


def clova_tts(text, lient_id=client_id, client_secret=client_secret, lang="Kor"):
    #
    # API : https://apidocs.ncloud.com/ko/ai-naver/clova_speech_synthesis/tts/
    # price : 4won/15sec 
    #
    url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
    encText = urllib.parse.quote(text)
    data = "speaker=mijin&speed=0&text=" + encText
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()

    if(rescode == 200):
        logger.log.info("Success Clova_tts")
        response_body = response.read()
        if os.path.exists(VOICE_DIR_PATH) == False:
            os.mkdir(VOICE_DIR_PATH)
        file_path = os.path.join(VOICE_DIR_PATH, utils.randome_file_name(TTS_FILE_NAME_LENGTH)+".mp3")
        with open(file_path, 'wb') as fd:
            fd.write(response_body)
        logger.log.info("TTS Voice File Saved to {}".format(file_path))
        return utils.play_mp3(file_path)
    else:
        logger.log.debug("Error clova_tts")
        return False
