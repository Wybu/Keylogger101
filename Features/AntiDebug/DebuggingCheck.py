from .RemoteDebugger import CheckRemoteDebugger
from .IsDebuggerPresent import is_debugger_present
from .CheckBlacklistedWindowsNames import CheckTitles

def IsDebugging():
    debugger_present_result = is_debugger_present()
    remote_debugger_result = CheckRemoteDebugger()
    blacklisted_names = CheckTitles()
    
    results = [
        debugger_present_result,
        remote_debugger_result,
        blacklisted_names
    ]

    if any(results) or all(results):
        return True
    
    return False
