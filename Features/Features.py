from Features.AntiDebug.DebuggingCheck import IsDebugging
from Features.AntiVirtulization.VirtualizingCheck import IsVirtualizing

class Features:
    def is_debugging(self):
        return IsDebugging()
    
    def is_virtualizing(self):
        return IsVirtualizing()