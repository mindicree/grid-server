import socket

# Developer Config
class Config():
    DEBUG = True
    HOST = 'localhost'
    PORT = 5001

# Test Config
# class Config():
#     DEBUG = False
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     HOST = s.getsockname()[0]
#     PORT = 80

# Deployment  Config
# class Config():
#     DEBUG = False
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     HOST = s.getsockname()[0]
#     PORT = 5001