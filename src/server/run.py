import subprocess

from server import drive as car
from server.sensor import server


def sensor_server():
    server.run_sensor_server()


def drive():
    car.run()

