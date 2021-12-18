import socket

class Config():
    DEBUG = True
    HOST = 'localhost'
    PORT = 5001

class DeployConfig():
    DEBUG = False
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    HOST = s.getsockname()[0]
    PORT = 80

class TestConfig():
    DEBUG = False
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    HOST = s.getsockname()[0]
    BACKEND = '192.168.50.17'
    PORT = 5001