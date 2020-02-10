import os
import subprocess
from aiy.board import Board
import aiy.voice.tts

def say(text):
    """
    text : 
    description : 
    """
    with Board() as board:
        aiy.voice.tts.say(text)


def say_korean(text):
    cmd = "espeak -v ko {}".format(text)
    return subprocess.check_call(cmd, shell=True)

