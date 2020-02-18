#-*- coding:utf-8 -*-
import os
import time
import threading
import subprocess
from aiy.board import Board, Led
from aiy.voice.audio import AudioFormat, record_file

from client import config, logger
from client.db import database
VOICE_DIR_PATH = os.path.join(config.VOICE_DIR_PATH, 'voices')

def randome_file_name(length:int)->str:
    """랜덤 문자열인 파일 이름을 생성한다.

    :param int length: 파일 이름 길이
    :returns: 랜덤 문자열 파일 이름
    """
    return database.create_random_string(length)


def voice_recoder(file_name:str)->str:
    """voices 폴더에 file_name으로 음성 파일을 녹음해 저장한다. 버튼을 누르면 음성 녹음이 종료된다.

    :param str file_name: 음성 파일을 저장할 파일 이름
    :returns: 음성 파일의 절대 경로, 실행 실패시 빈 문자열을 리턴한다.
    """
    if os.path.exists(VOICE_DIR_PATH) == False:
        os.mkdir(VOICE_DIR_PATH)

    file_path = os.path.join(VOICE_DIR_PATH, file_name)
    logger.log.info("[voice/utils.py:voice_recoder] Recording... {}".format(file_path))
    
    try:
        with Board() as board: 
            done = threading.Event()
            board.button.when_pressed = done.set

            def wait():
                board.led.state = Led.ON
                start = time.monotonic()
                while not done.is_set():
                    duration = time.monotonic() - start
                    logger.log.info('[voice/utils.py:voice_recoder] Recording: %.02f seconds [Press button to stop]' % duration)
                    time.sleep(0.5)

            record_file(AudioFormat.CD, filename=file_path, wait=wait, filetype='wav')
            board.led.state = Led.OFF
            logger.log.info('[voice/utils.py:voice_recoder] Recording finished ...')
    except Exception as e:
        logger.log.error("[voice/utils.py:voice_recoder][E] {}".format(e))
        return ""
    else:
        return file_path


def play_mp3(file_path:str)->bool:
    """mp3형식의 오디오 파일을 mpg123를 이용해 실행한다.

    :param str file_path: 오디오 파일의 경로
    :returns: bool타입의 함수 실행 결과
    """
    cmd = ['mpg123', file_path]
    if os.path.exists(file_path):
        logger.log.info("[voice/utils.py:play_mp3] play mp3 with mpg123 {}".format(file_path))
        try:
            with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
                logger.log.info(proc.stdout.read())
        except Exception as e:
            logger.log.error("[voice/utils.py:play_mp3][E] {}".format(e))
            return False
        else:
            return True
    else:
        logger.log.error("[voice/utils.py:play_mp3][E] " + \
            "No Such File {}".format(file_path))
        return False
