# main.py
import socket
import time
from shell import shell

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
