import socket
import logging
import re

# server to listen from
PORT = 5050
# local IP address
SERVER = socket.gethostbyname("localhost")

ADDRESS = (SERVER,PORT)
logging.basicConfig(filename='result.txt',level=logging.INFO)


def is_valid_operation(operation):
    # pattern: optional leading white spaces followed by an optional "-" (for negative numbers), 
    # followed by one or more digits, then any number of groups that consist of: 
    # white spaces, an operator (+, -, *, /), white spaces, optional "-" (for negative numbers), 
    # and one or more digits, ending with optional trailing white spaces
    pattern = r"^\s*-?\d+(?:\s*[-+*/]\s*-?\d+)*\s*$"
    return bool(re.match(pattern, operation))
try:
    # data to send
    # with open("op_test.txt", "r") as file:
    #     operations = file.readlines()

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        sock.connect(ADDRESS)
        operations = []
        with open("operations.txt", "r") as file:
            operations = file.readlines()
            
        for i in range(0, len(operations), 3):  # iterate over operations in groups of 3
            operation_batch = [op.rstrip('\n') for op in operations[i:i+3]]
            operations_str = '|'.join(operation for operation in operation_batch if is_valid_operation(operation))
            sock.sendall(operations_str.encode()) 
            data = sock.recv(1024)
            for operation, result in zip(operation_batch, data.decode().split('|')):
                logging.info(operation + ' = ' + result)
except FileNotFoundError:
    logging.error("File not found.")
except ConnectionError:
    logging.error("Connection error.")
except Exception as e:
    logging.error(f"An error occurred: {e}")