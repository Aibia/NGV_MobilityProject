import signal
import time
from multiprocessing import Process
from server import drive as car
from server import sensor_server
from server import logger, config


class Server:
    ## TODO
    ## signal & terminate
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super( Server, self).__new__(self)
        return self.instance


    def __init__(self):
        self.server_process = Process(target=sensor_server.run_sensor_server)
        self.drive_process = Process(target=car.run)
        signal.signal(signal.SIGINT, self.stop)


    def start(self):
        logger.log.info("[server.py:run] Start server ... ")
        if self.server_process.is_alive() == False:
            self.server_process.start()
            time.sleep(3)
        if self.drive_process.is_alive() == False:
            self.drive_process.start()
        return True
    

    def stop(self, sig, frame):
        logger.log.info("[server.py:stop] Stop server ...")
        if self.server_process.is_alive():
            self.server_process.terminate()
        if self.drive_process.is_alive():
            self.drive_process.terminate()
        logger.log.info("[server.py:stop] Server Stopped!")
        return True


    def is_alive(self):
        server_process_is_alive = self.server_process.is_alive()
        drive_process_is_alive = self.drive_process.is_alive()
        if server_process_is_alive or drive_process_is_alive:
            if server_process_is_alive:
                logger.log.info("[server.py:is_alive] Sensor Server is alive!")
            if drive_process_is_alive:
                logger.log.info("[server.py:is_alive] Drive Process is alive!")
            return True
        return False