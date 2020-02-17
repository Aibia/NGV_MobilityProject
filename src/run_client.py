import signal
from client.client import Client
        

signal.signal(signal.SIGINT, Client().stop)
client = Client()
client.start()