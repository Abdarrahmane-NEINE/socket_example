# Multiprocessing Arithmetic Service with Socket

## Overview
This project is a simple arithmetic service built in Python that demonstrates inter-process communication without using the `multiprocessing` module. The service uses sockets to receive arithmetic operations from a client, spawns child processes (using `os.fork()`) to compute the results, and sends the results back to the client. All inter-process communication is handled via pipes, and logging is used for error tracking and debugging.

## Features
- **Socket Communication:**  
  The server listens for client connections on a specified port (5050) and receives arithmetic operations.

- **Dynamic Process Management:**  
  The parent process creates and destroys child processes for each operation. Each child process calculates the result and exits after sending its result back to the parent via pipes.

- **Inter-Process Communication:**  
  Pipes are used for exchanging data between the parent and child processes.

- **Secure Arithmetic Evaluation:**  
  Arithmetic operations are parsed and computed without using `eval()`.

- **Logging:**  
  Both the server and client log errors and results to files (`server_log.txt` and `result.txt` respectively).

## Requirements
- **Python 3.x**  
- **Unix-like OS:**  
  The use of `os.fork()` and pipes makes this project best suited for Unix-like operating systems.

## Running the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/Abdarrahmane-NEINE/socket_example.git

### Server
1. Ensure that the server and client scripts are in the same directory.
2. Start the server:
   ```bash
   python server.py
