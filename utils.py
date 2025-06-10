import os

def os_specific(ifWindows, ifLinuxMacOs, ifOtherOs=lambda: print("none")):
    if os.name == 'nt':
        ifWindows()
    elif os.name == 'posix':
        ifLinuxMacOs()
    else:
        ifOtherOs()