#!/usr/bin/env python3
#
# The Raspberry Pi panel controller is the client part of IoT panel advertising project.
# This is a local controlletr for RPi which use PanelDisplay as a handler for local manipulations.
#
import os
import sys
import logging
import subprocess
import collections
import configparser
import datetime
from time import time
from pathlib import Path
from threading import Thread

from matrix_config import MatrixConfig
from panel import PanelDisplay
import common


#--------------------------------------------------------------
# In terminal UI methods

def showHelp():
    print ("---------------------------------------------\n"
           " q/quit     : Quit the program\n"
           " h/help     : Show help \n"
           " di/d-image : Display the current file as an image \n"
           " dv/d-video : Display the current file as a video \n"
           " dt/d-text  : Display the scrolling text from file \n"
           " s/stop     : Stop displaying\n"
           " r/restart  : Display from the beginning\n"
           " f/file     : set file name \n"
           " k/killall  : kill all other running viewers \n"
           " c/showconf : Show current configurations \n"
           " rc/reloadconf : Reload configuration file \n"
           "---------------------------------------------\n")
    
def userCommandDict(cmd):
    switcher={
        "h":"HELP",
        "help":"HELP",
        "q":"QUIT",
        "quit":"QUIT",
        "di":"VIEW-IMAGE",
        "d-image":"VIEW-IMAGE",
        "dv":"VIEW-VIDEO",
        "d-video":"VIEW-VIDEO",
        "dt":"VIEW-TEXT",
        "d-text":"VIEW-TEXT",
        "r":"RESTART",
        "restart":"RESTART",
        "s":"STOP",
        "stop":"STOP",
        "f":"FILE",
        "file":"FILE",
        "k":"KILLALL",
        "killall":"KILLALL",
        "c":"SHOWCONFIG",
        "showconf":"SHOWCONFIG",
        "rc":"RELOADCONFIG",
        "reloadconf":"RELOADCONFIG"
    }
    return switcher.get(cmd,"Invalid request")


#--------------------------------------------------------------
# Main thread

def main():
    logging.basicConfig(filename='/home/pi/src/rpi-panel-controller/logs/'+datetime.datetime.now().strftime("%Y%m%d")+'.log'
        , level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logging.info('')
    logging.info('Started')
    ts = time()
    try:
        th_panel = PanelDisplay(1, "Th-display")
    except:
        logging.info("Error: unable to create thread")

    showHelp()
    
    while True:
        cmd = input().lower()
        if userCommandDict(cmd) == "HELP":
            showHelp()
        if userCommandDict(cmd) == "QUIT":
            killed = common.killAll()
            if killed > 0:
                logging.info(str(killed)+" running viewer(s) already exist..")
            break
        elif userCommandDict(cmd) == "VIEW-IMAGE":
            th_panel.play(userCommandDict(cmd))
        elif userCommandDict(cmd) == "VIEW-VIDEO":
            th_panel.play(userCommandDict(cmd))
        elif userCommandDict(cmd) == "VIEW-TEXT":
            th_panel.play(userCommandDict(cmd))
        elif userCommandDict(cmd) == "RESTART":
            th_panel.restart()
        elif userCommandDict(cmd) == "STOP":
            th_panel.terminate()
        elif userCommandDict(cmd) == "FILE":
            th_panel.filename = input("enter the file name: ")
        elif userCommandDict(cmd) == "KILLALL":
            killed = common.killAll()
            if killed > 0:
                logging.info(str(killed)+" running viewer(s) already exist..")
        elif userCommandDict(cmd) == "SHOWCONFIG":
            th_panel.matrixConfig.displayConfigs()
        elif userCommandDict(cmd) == "RELOADCONFIG":
            th_panel.matrixConfig.reloadMatrixConfigs()
            print('Matrix config file reloaded: ', th_panel.matrixConfig.configFilePath)
      
    logging.info('Exiting Main Thread : Took %s', time() - ts)
    logging.info('Finished')


if __name__ == '__main__':
    main()

#--------------------------------------------------------------
