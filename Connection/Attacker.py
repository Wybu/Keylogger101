import socket

def start_server(host='0.0.0.0', port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"Listening on {host}:{port}...")

    conn, addr = server.accept()
    print(f"Connection established with {addr}")

    while True:
        command = input("Enter command to execute: ")
        if command.lower() == 'exit':
            conn.send(command.encode())
            break
        conn.send(command.encode())
        output = conn.recv(4096).decode('utf-8')
        print(f"Output: {output}")

    conn.close()

if __name__ == "__main__":
    start_server()
