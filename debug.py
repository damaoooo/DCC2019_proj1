import socket
sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sk.bind(('127.0.0.1',56842))
dest = ('127.0.0.1',56841)
