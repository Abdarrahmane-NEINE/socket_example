import socket

# server to listen from
PORT = 5050
# local IP address
SERVER = socket.gethostbyname("localhost")

ADDRESS = (SERVER,PORT)

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
    sock.connect(ADDRESS)
    sock.sendall(b'Hello world')
    data = sock.recv(1024)
print("Received = ",repr(data))