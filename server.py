import socket
import logging
from multiprocessing import Process, Pipe

# server to listen from
PORT = 5050
# local IP address
SERVER = socket.gethostbyname("localhost")

ADDRESS = (SERVER,PORT)

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
    sock.bind(ADDRESS)
    # listen only to 1 client
    sock.listen(1)
    connection, addr = sock.accept()
    with connection:
        print('connected by', addr)
        while True:
            data = connection.recv(1024)
            if not data: break
            print('data = ',data)
            connection.sendall(data)
