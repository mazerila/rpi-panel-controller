#!/usr/bin/env python3
#
# The Raspberry Pi panel controller is the client part of IoT panel advertising project.
# This is the main file of the project.
#
import os
import sys
import logging
import collections
import configparser
import subprocess
import signal
from time import time
from pathlib import Path
from threading import Thread

from matrix_config import MatrixConfig
import common

#--------------------------------------------------------------
# todo: 
# 1. receive commands from server
# 2. apply received commands
# 3. separate log files by date
#--------------------------------------------------------------


class PanelDisplay (Thread):
    proc = None
    filename = "/home/pi/src/samples/gif16-6.gif"
    contentType = "VIEW-IMAGE"
    matrixConfig = MatrixConfig()

    def __init__(self, threadID, name):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def terminate(self): 
        self._running = False
        if self.proc != None and self.proc.poll() == None:
            print("Stopping")
            # Send the signal to all the process groups
            output = os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
            logging.info(output)
            self.proc = None

    def play(self, cType):
        self.contentType = cType
        self.run()
		
    def    run(self):
        if self.proc == None or self.proc.poll() != None:
            self.display();
        else:
            print("The panel is already busy!")

    def restart(self):
        print("Restarting")
        if self.proc != None:
            self.terminate();
        self.display()

    def display(self):
        if self.filename == "":
            print("filename not set!")
            return

        if self.contentType == "VIEW-IMAGE":
            viewer="/home/pi/src/rpi-rgb-led-matrix/utils/led-image-viewer"
        elif self.contentType == "VIEW-VIDEO":
            viewer="/home/pi/src/rpi-rgb-led-matrix/utils/video-viewer"    
        elif self.contentType == "VIEW-TEXT":
            viewer="/home/pi/src/rpi-rgb-led-matrix/utils/text-scroller"            

        print (viewer, "Displaying the file: ", self.filename)
        logging.info("Displaying the file: " + self.filename)
        
        cmd_params = list([viewer])
        if 'led-panel-width' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-cols="+self.matrixConfig.sectionDict['GENERAL']['led-panel-width']])
        if 'led-panel-height' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-rows="+self.matrixConfig.sectionDict['GENERAL']['led-panel-height']])
        if 'led-chain' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-chain="+self.matrixConfig.sectionDict['GENERAL']['led-chain']])
        if 'led-parallel' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-parallel="+self.matrixConfig.sectionDict['GENERAL']['led-parallel']])
        if 'led-pwm-bits' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-pwm-bits="+self.matrixConfig.sectionDict['GENERAL']['led-pwm-bits']])
        if 'led-multiplexing' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-multiplexing="+self.matrixConfig.sectionDict['GENERAL']['led-multiplexing']])
        if 'led-brightness' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-brightness="+self.matrixConfig.sectionDict['GENERAL']['led-brightness']])
        if 'led-pixel-mapper' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-pixel-mapper="+self.matrixConfig.sectionDict['GENERAL']['led-pixel-mapper']])
        if 'led-gpio-mapping' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-gpio-mapping="+self.matrixConfig.sectionDict['GENERAL']['led-gpio-mapping']])
        if 'led-scan-mode' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-scan-mode="+self.matrixConfig.sectionDict['GENERAL']['led-scan-mode']])
        if 'led-row-addr-type' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-row-addr-type="+self.matrixConfig.sectionDict['GENERAL']['led-row-addr-type']])
        if 'led-show-refresh' in self.matrixConfig.sectionDict['GENERAL'].keys():
            if common.getboolean(self.matrixConfig.sectionDict['GENERAL']['led-show-refresh']):
                cmd_params.extend(["--led-show-refresh"])
        if 'led-limit-refresh' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-limit-refresh="+self.matrixConfig.sectionDict['GENERAL']['led-limit-refresh']])
        if 'led-inverse' in self.matrixConfig.sectionDict['GENERAL'].keys():
            if common.getboolean(self.matrixConfig.sectionDict['GENERAL']['led-inverse']):
                cmd_params.extend(["--led-inverse"])
        if 'led-rgb-sequence' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-rgb-sequence="+self.matrixConfig.sectionDict['GENERAL']['led-rgb-sequence']])
        if 'led-pwm-lsb-nanoseconds' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-pwm-lsb-nanoseconds="+self.matrixConfig.sectionDict['GENERAL']['led-pwm-lsb-nanoseconds']])
        if 'led-pwm-dither-bits' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-pwm-dither-bits="+self.matrixConfig.sectionDict['GENERAL']['led-pwm-dither-bits']])
        if 'led-no-hardware-pulse' in self.matrixConfig.sectionDict['GENERAL'].keys():
            if common.getboolean(self.matrixConfig.sectionDict['GENERAL']['led-no-hardware-pulse']):
                cmd_params.extend(["--led-no-hardware-pulse"])
        if 'led-panel-type' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-panel-type="+self.matrixConfig.sectionDict['GENERAL']['led-panel-type']])
        if 'led-slowdown-gpio' in self.matrixConfig.sectionDict['GENERAL'].keys():
            cmd_params.extend(["--led-slowdown-gpio="+self.matrixConfig.sectionDict['GENERAL']['led-slowdown-gpio']])
        
        
        if self.contentType == "VIEW-IMAGE": 
            if 'image-center' in self.matrixConfig.sectionDict['IMAGE'].keys():
                if common.getboolean(self.matrixConfig.sectionDict['IMAGE']['image-center']):
                    cmd_params.extend(["-C"])
            if 'image-wait' in self.matrixConfig.sectionDict['IMAGE'].keys():
                cmd_params.extend(["-w"+self.matrixConfig.sectionDict['IMAGE']['image-wait']])
            if 'image-time' in self.matrixConfig.sectionDict['IMAGE'].keys():
                cmd_params.extend(["-t"+self.matrixConfig.sectionDict['IMAGE']['image-time']])
            if 'image-loop' in self.matrixConfig.sectionDict['IMAGE'].keys():
                cmd_params.extend(["-l"+self.matrixConfig.sectionDict['IMAGE']['image-loop']])
            if 'image-delay' in self.matrixConfig.sectionDict['IMAGE'].keys():
                cmd_params.extend(["-D"+self.matrixConfig.sectionDict['IMAGE']['image-delay']])
            if 'image-vsync-multiple' in self.matrixConfig.sectionDict['IMAGE'].keys():
                cmd_params.extend(["-V"+self.matrixConfig.sectionDict['IMAGE']['image-vsync-multiple']])
            if 'image-forever-cycle' in self.matrixConfig.sectionDict['IMAGE'].keys():
                if common.getboolean(self.matrixConfig.sectionDict['IMAGE']['image-forever-cycle']):
                    cmd_params.extend(["-f"])
            if 'image-shuffle' in self.matrixConfig.sectionDict['IMAGE'].keys():
                if common.getboolean(self.matrixConfig.sectionDict['IMAGE']['image-shuffle']):
                    cmd_params.extend(["-s"])
            cmd_params.extend([self.filename])


        elif self.contentType == "VIEW-VIDEO": 
            if 'video-fullscreen' in self.matrixConfig.sectionDict['VIDEO'].keys():
                if common.getboolean(self.matrixConfig.sectionDict['VIDEO']['video-fullscreen']):
                    cmd_params.extend(["-F"])
            if 'video-skip-frames' in self.matrixConfig.sectionDict['VIDEO'].keys():
                cmd_params.extend(["-s"+self.matrixConfig.sectionDict['VIDEO']['video-skip-frames']])
            if 'video-max-frames' in self.matrixConfig.sectionDict['VIDEO'].keys():
                cmd_params.extend(["-c"+self.matrixConfig.sectionDict['VIDEO']['video-max-frames']])
            if 'video-vsync-multiple' in self.matrixConfig.sectionDict['VIDEO'].keys():
                cmd_params.extend(["-V"+self.matrixConfig.sectionDict['VIDEO']['video-vsync-multiple']])
            if 'video-verbose' in self.matrixConfig.sectionDict['VIDEO'].keys():
                if common.getboolean(self.matrixConfig.sectionDict['VIDEO']['video-verbose']):
                    cmd_params.extend(["-v"])
            if 'video-loop' in self.matrixConfig.sectionDict['VIDEO'].keys():
                if common.getboolean(self.matrixConfig.sectionDict['VIDEO']['video-loop']):
                    cmd_params.extend(["-f"])
            cmd_params.extend([self.filename])


        elif self.contentType == "VIEW-TEXT": 
            if 'text-speed' in self.matrixConfig.sectionDict['TEXT'].keys():
                cmd_params.extend(["-s"+self.matrixConfig.sectionDict['TEXT']['text-speed']])
            if 'text-loop-count' in self.matrixConfig.sectionDict['TEXT'].keys():
                cmd_params.extend(["-l"+self.matrixConfig.sectionDict['TEXT']['text-loop-count']])
            if 'text-font-file' in self.matrixConfig.sectionDict['TEXT'].keys():
                cmd_params.extend(["-f"+self.matrixConfig.sectionDict['TEXT']['text-font-file']])
            if 'text-brightness' in self.matrixConfig.sectionDict['TEXT'].keys():
                cmd_params.extend(["-b"+self.matrixConfig.sectionDict['TEXT']['text-brightness']])
            if 'text-x-origin' in self.matrixConfig.sectionDict['TEXT'].keys():
                cmd_params.extend(["-x"+self.matrixConfig.sectionDict['TEXT']['text-x-origin']])
            if 'text-y-origin' in self.matrixConfig.sectionDict['TEXT'].keys():
                cmd_params.extend(["-y"+self.matrixConfig.sectionDict['TEXT']['text-y-origin']])
            if 'text-track-spacing' in self.matrixConfig.sectionDict['TEXT'].keys():
                cmd_params.extend(["-t"+self.matrixConfig.sectionDict['TEXT']['text-track-spacing']])
            if 'text-font-color' in self.matrixConfig.sectionDict['TEXT'].keys():
                cmd_params.extend(["-C"+self.matrixConfig.sectionDict['TEXT']['text-font-color']])
            if 'text-background-color' in self.matrixConfig.sectionDict['TEXT'].keys():
                cmd_params.extend(["-B"+self.matrixConfig.sectionDict['TEXT']['text-background-color']])
            if 'text-outline-color' in self.matrixConfig.sectionDict['TEXT'].keys():
                cmd_params.extend(["-O"+self.matrixConfig.sectionDict['TEXT']['text-outline-color']])
            with open(self.filename, encoding='utf-8') as textfile:
                content = textfile.read()
            cmd_params.extend(["\""+content+"\""])

                
        cmd = " ".join(cmd_params)
        # The os.setsid() is passed in the argument preexec_fn so
        # it's run after the fork() and before  exec() to run the shell.
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)


#--------------------------------------------------------------
# Global vriables


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

def get_pid(name):
    try:
        pids = subprocess.check_output(["pidof",name])
    except:
        return list()

    return list(map(int,pids.split()))

def killAll():
    # ps -A | grep viewer
    pidList = get_pid("video-viewer")
    pidList.extend(get_pid("led-image-viewer"))
    pidList.extend(get_pid("text-scroller"))
    
    if len(pidList)>0:
        logging.info(str(len(pidList))+" running viewer(s) already exist..")
    for pid in pidList:
        os.kill(pid, signal.SIGKILL)
    
#--------------------------------------------------------------
# Main thread

def main():
    logging.basicConfig(filename='/home/pi/src/rpi-panel-controller/logs/controller.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
            killAll()
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
            killAll()
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
