import socket
import threading
import time
import queue

def get_local_ip():
    """Get the local IP address of the machine running the program."""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def simulate_malware_spread(sock, network_prefix=None, target_port=80, start_ip=1, end_ip=100, delay=0.1):
    """
    Simulate malware spreading across the network and send results back to the server.
    """
    # If no network prefix is provided, use the prefix from the local IP
    if network_prefix is None:
        local_ip = get_local_ip()
        network_prefix = ".".join(local_ip.split(".")[:-1])  # Example: '192.168.1'
    elif len(network_prefix.split(".")) == 4:
        network_prefix = ".".join(network_prefix.split(".")[:-1])  # Giữ lại 3 octet đầu

    threads = []
    results = queue.Queue()  # Sử dụng hàng đợi để thu thập kết quả

    def thread_target(ip):
        """Thread function for scanning and infection."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((ip, target_port))
                if result == 0:
                    message = f"[+] Found open port on {ip}. Simulating infection..."
                    results.put(message)  # Thêm kết quả vào hàng đợi
                    sock.sendall(b"Simulated malware payload")
                else:
                    message = f"[-] Could not connect to {ip}."
                    results.put(message)  # Thêm kết quả vào hàng đợi
        except Exception as e:
            results.put(f"[-] Error scanning {ip}: {e}")

    # Scan from IP x.x.x.start_ip to x.x.x.end_ip
    for i in range(start_ip, end_ip + 1):
        ip = f"{network_prefix}.{i}"
        thread = threading.Thread(target=thread_target, args=(ip,))
        thread.start()
        threads.append(thread)
        time.sleep(delay)

    for thread in threads:
        thread.join()  # Đợi tất cả các thread hoàn thành

    # Gửi tất cả kết quả về server
    all_results = []  # Danh sách để lưu trữ tất cả kết quả
    while not results.empty():  # Kiểm tra hàng đợi không rỗng
        result = results.get()
        all_results.append(result)  # Thêm kết quả vào danh sách

    # Gửi tất cả các kết quả cùng một lần
    if all_results:
        sock.sendall("\n".join(all_results).encode() + b'\n')  # Gửi tất cả kết quả
