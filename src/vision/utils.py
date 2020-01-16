import numpy as np

def reshape(array, width):
    assert len(array) % width == 0
    height = len(array) // width
    return [array[i * width:(i+1) * width] for i in range(height)]



