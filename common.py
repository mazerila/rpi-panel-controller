#
# Common functionalities required in the project
#
import os
import sys
import signal
import subprocess
import collections

def getboolean(val:str):
    if (val.lower() == 'yes' or val.lower() == 'true' 
        or val.lower() == 'on' or val.lower() == '1' ):
        return True
    return False

def get_pid(name):
    try:
        pids = subprocess.check_output(["pidof",name])
    except:
        return list()

    return list(map(int,pids.split()))

def killAll():
    # ps -A | grep viewer
    pidList = get_pid("p-video-viewer")
    pidList.extend(get_pid("p-image-viewer"))
    pidList.extend(get_pid("p-text-scroller"))
    ret = len(pidList)
    for pid in pidList:
        os.kill(pid, signal.SIGKILL)
    return ret
    