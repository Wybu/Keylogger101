import socket

# Tạo server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Địa chỉ IP và cổng mà server sẽ lắng nghe
ServIP = "127.0.0.1"  # Lắng nghe trên tất cả các địa chỉ IP (0.0.0.0)
ServPort = 50000     # Cổng để kết nối

# Bind server tới IP và cổng
server.bind((ServIP, ServPort))

# Đặt server vào trạng thái lắng nghe
server.listen(1)
print(f"Đang lắng nghe kết nối từ client trên {ServIP}:{ServPort}...")

# Chấp nhận kết nối từ client
client_socket, client_address = server.accept()
print(f"Đã kết nối với client: {client_address}")

# Vòng lặp để gửi lệnh đến client
while True:
    command = input("Nhập lệnh để gửi đến client (gõ 'exit' để thoát): ")

    if command.strip().lower() == "exit":
        client_socket.send("exit".encode())  # Gửi lệnh 'exit' để ngắt kết nối client
        break

    # Gửi lệnh đến client
    client_socket.send(command.encode())

    # Nhận kết quả từ client
    result = client_socket.recv(4096).decode()

    print(f"Kết quả từ client:\n{result}")

# Đóng kết nối
client_socket.close()
server.close()
