import os
import time
import threading
from aiy.board import Board, Led
from aiy.voice.audio import AudioFormat, record_file

from client import config, logger
from client.db import database
VOICE_DIR_PATH = os.path.join(config.VOICE_DIR_PATH, 'voices')

def randome_file_name(LENGTH):
    return database.create_random_string(LENGTH)

def voice_recoder(FILE_NAME):
    if os.path.exists(VOICE_DIR_PATH) == False:
        os.mkdir(VOICE_DIR_PATH)

    file_path = os.path.join(VOICE_DIR_PATH, FILE_NAME)
    logger.log.info("Recording... {}".format(file_path))
    
    with Board() as board: 
        done = threading.Event()
        board.button.when_pressed = done.set

        def wait():
            board.led.state = Led.ON
            start = time.monotonic()
            while not done.is_set():
                duration = time.monotonic() - start
                logger.log.info('Recording: %.02f seconds [Press button to stop]' % duration)
                time.sleep(0.5)

        
        record_file(AudioFormat.CD, filename=file_path, wait=wait, filetype='wav')
        board.led.state = Led.OFF
        logger.log.info('Recording finished ...')
    return file_path

def play_mp3(file_path):
    if os.path.exists(file_path):
        logger.log.info("Play mp3 with mpg123 {}".format(file_path))
        return os.system('mpg123 ' +file_path)
    else:
        logger.log.debug("Error No Such File {}".format(file_path))
        return False
