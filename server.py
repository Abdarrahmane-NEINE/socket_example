import socket
import os
import logging

# server to listen from
PORT = 5050
# local IP address
SERVER = socket.gethostbyname("localhost")

ADDRESS = (SERVER,PORT)

logging.basicConfig(filename='server_log.txt',level=logging.INFO)

MAX_PROCESSES = 4  # change to a suitable number for your system

def calculateOperation(operation):
    try:
        operation = operation.split()
        while "*" in operation or "/" in operation:
            for i in range(len(operation)):
                if operation[i] == "*":
                    result = float(operation[i-1]) * float(operation[i+1])
                    operation[i-1] = result
                    del operation[i:i+2]
                    break
                elif operation[i] == "/":
                    result = float(operation[i-1]) / float(operation[i+1])
                    operation[i-1] = result
                    del operation[i:i+2]
                    break
        while "+" in operation or "-" in operation:
            for i in range(len(operation)):
                if operation[i] == "+":
                    result = float(operation[i-1]) + float(operation[i+1])
                    operation[i-1] = result
                    del operation[i:i+2]
                    break
                elif operation[i] == "-":
                    result = float(operation[i-1]) - float(operation[i+1])
                    operation[i-1] = result
                    del operation[i:i+2]
                    break
        return result
    except ValueError:
        logging.error(f"Invalid operation: {operation}")
        return 0
    except ZeroDivisionError as z:
        logging.error(z)
        return 0
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return 0


try:
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        sock.bind(ADDRESS)
        # listen only to 1 client
        sock.listen(1)
        connection, client_address = sock.accept()
        with connection:
            while True:
                data = connection.recv(1024)
                if not data: 
                    break
                # split the operations
                operations = data.decode().split('|')

                results = []  # this will hold the results from each process
                child_processes = [None] * MAX_PROCESSES
                child_pipes = [None] * MAX_PROCESSES

                for operation in operations:
                    # find an available child process
                    for i in range(MAX_PROCESSES):
                        if child_processes[i] is None or os.waitpid(child_processes[i], os.WNOHANG) != (0, 0):
                            # this child process is available
                            break
                    else:
                        # all child processes are busy, wait for one to finish
                        pid, _ = os.wait()
                        i = child_processes.index(pid)

                    # if this child process was previously used, close its old pipe
                    if child_pipes[i] is not None:
                        os.close(child_pipes[i])

                    # create a new pipe for this child process
                    parent_conn, child_conn = os.pipe()
                    child_pipes[i] = parent_conn

                    new_process_id = os.fork()
                    if new_process_id == 0:  # child process
                        os.close(parent_conn)
                        result = calculateOperation(operation)
                        os.write(child_conn, str(result).encode())
                        os.close(child_conn)
                        os._exit(0)  # terminate the child process

                    # parent process
                    child_processes[i] = new_process_id
                    os.close(child_conn)

                # wait for all child processes to finish
                for i in range(MAX_PROCESSES):
                    if child_processes[i] is not None:
                        os.waitpid(child_processes[i], 0)
                        result = os.read(child_pipes[i], 1024).decode()  # added the decode call
                        results.append(result)
                        os.close(child_pipes[i])

                # send all results back to the client
                connection.sendall('|'.join(results).encode())
            connection.close()
except OSError as e:
    if e.errno == 24:
        logging.error("Too many open files.")
    else:
        logging.error(f"OS error: {e}")
except Exception as e:
    logging.error(f"An error occurred: {e}")
