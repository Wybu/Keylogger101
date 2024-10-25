from .TriageCheck import TriageCheck
from .UsernameCheck import CheckForBlacklistedNames
from .VMArtifacts import VMArtifactsDetect
from .VMWareDetection import GraphicsCardCheck as VMWareGraphicsCardCheck
from .VirtualboxDetection import GraphicsCardCheck as VirtualboxGraphicsCardCheck
from .QEMUCheck import CheckForQEMU
from .ParallelsCheck import CheckForParallels
from .MonitorMetrics import IsScreenSmall 
from .KVMCheck import CheckForKVM 
from .RecentFileActivity import RecentFileActivityCheck

def IsVirtualizing():
    triage_result = TriageCheck()
    rec_file_result, _ = RecentFileActivityCheck()
    username_result = CheckForBlacklistedNames()
    vm_result = VMArtifactsDetect()
    vmware_result = VMWareGraphicsCardCheck()
    virtualbox_result = VirtualboxGraphicsCardCheck()
    qemu_result, _ = CheckForQEMU()
    parallels_result, _ = CheckForParallels()
    screen_small_result, _ = IsScreenSmall()
    kvm_result, _ = CheckForKVM()

    results = [
        triage_result,
        rec_file_result,
        username_result,
        vm_result,
        vmware_result,
        virtualbox_result,
        qemu_result,
        parallels_result,
        screen_small_result,
        kvm_result
    ]

    if any(results) or all(results):
        return True
    
    return False
