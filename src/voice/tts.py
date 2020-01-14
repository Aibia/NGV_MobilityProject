from aiy.board import Board
import aiy.voice.tts


def say(text):
    with Board() as board:
        aiy.voice.tts.say(text)

