from aiy.board import Board, Led
import time
import os
import threading
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder
from client import config, logger

VOICE_DIR_PATH = os.path.join(config.VOICE_DIR_PATH, 'voices')

def voice_recoder():
    file_path = os.path.join(VOICE_DIR_PATH, "voice.wav")

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
    return file_path

def play_mp3(file_path):
    if os.path.exists(file_path):
        return os.system('mpg123 ' +file_path)
    else:
        return False
