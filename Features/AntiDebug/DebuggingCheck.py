from .IsDebuggerPresent import is_debugger_present
from .RemoteDebugger import CheckRemoteDebugger
from .ParentAntiDebug import ParentAntiDebug

def IsDebugging():
    debugger_present_result = is_debugger_present()
    remote_debugger_result = CheckRemoteDebugger()
    parent_anti_debug_result = ParentAntiDebug()
    
    results = [
        debugger_present_result,
        remote_debugger_result,
        parent_anti_debug_result
    ]

    if any(results) or all(results):
        return True
    
    return False
