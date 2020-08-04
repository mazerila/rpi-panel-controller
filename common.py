#
# Common functionalities required in the project
#
import os
import sys
import signal
import logging
import datetime
import subprocess
import collections
from pathlib import Path

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
    
def setLogger():
    logPath = '/home/pi/src/rpi-panel-controller/logs/'
    Path(logPath).mkdir(parents=True, exist_ok=True) 
    logging.basicConfig(filename=logPath+datetime.datetime.now().strftime("%Y%m%d")+'.log'
        , level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logging.info('')
   