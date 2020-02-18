import signal
from multiprocessing import Process
from server import drive as car
from server import sensor_server
from server import logger, config


class Server:
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super( Server, self).__new__(self)
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
        logger.log.info("Server Stopped!")
        return True


    def is_alive(self):
        server_process_is_alive = self.server_process.is_alive()
        drive_process_is_alive = self.drive_process.is_alive()
        if server_process_is_alive or drive_process_is_alive:
            if server_process_is_alive:
                logger.log.info("Sensor Server is alive!")
            if drive_process_is_alive:
                logger.log.info("Drive Process is alive!")
            return True
        return False


signal.signal(signal.SIGINT, Server().stop)

server_process = Server()
server_process.run()
    
