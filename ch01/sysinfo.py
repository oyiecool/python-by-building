# sysinfo.py - print a quick report about this computer
import platform
import os
import getpass
from datetime import datetime

print("=" * 40)
print(" SYSTEM REPORT")
print("=" * 40)
print("Date/time :", datetime.now().strftime("%Y-%m-%d %H:%M"))
print("User      :", getpass.getuser())
print("Hostname  :", platform.node())
print("OS        :", platform.system(), platform.release())
print("Machine   :", platform.machine())
print("CPU cores :", os.cpu_count())
print("Python    :", platform.python_version())
print("Folder    :", os.getcwd())
