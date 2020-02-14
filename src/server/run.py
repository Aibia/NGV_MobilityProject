import signal
from multiprocessing import Process
from server import drive as car
from server import sensor_server
from sensor import logger, config


class ServerProcess:
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super( ServerProcess, self).__new__(self)
        return self.instance


    def __init__(self):
        self.server_process = Process(target=sensor_server.run_sensor_server)
        self.drive_process = Process(target=car.run)


    def run(self):
        logger.log.info("Start server ... ")
        if self.server_process.is_alive() == False:
            self.server_process.start()
        if self.drive_process.is_alive():
            self.drive_process.start()
        return True
    

    def stop(self, sig, frame):
        logger.log.info("Stop server ...")
        if self.server_process.is_alive():
            self.server_process.kill()
        if self.drive_process.is_alive():
            self.drive_process.terminate()
        return True


    def is_alive(self):
        if self.server_process.is_alive() or self.drive_process.is_alive():
            return True
        return False

signal.signal(signal.SIGINT, ServerProcess().stop)

server_process = ServerProcess()
server_process.run()
    
