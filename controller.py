#!/usr/bin/env python3
#
# The Raspberry Pi panel controller is the client part of IoT panel advertising project.
# This is the main file of the project which could communicate with the Azure server to send 
# telemetry and receive commands and execute them using PanelDisplay.
#
import os
import sys
import json
import random
import logging
import asyncio
import datetime
import subprocess
import collections
import configparser
import signal
from time import time
from pathlib import Path
from threading import Thread

from matrix_config import MatrixConfig
from device_config import DeviceConfig
import common

from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import MethodResponse
from azure.iot.device import Message
#--------------------------------------------------------------
# todo: 
# 1. receive commands from server
# 2. apply received commands
#--------------------------------------------------------------


#--------------------------------------------------------------
# Global vriables


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
