#!/usr/bin/env python3
#
# This class is in charge of controlling the panel as an API
#
import os
import sys
import logging
import subprocess
import collections
import configparser
import signal
from time import time
from pathlib import Path
from threading import Thread

from matrix_config import MatrixConfig
import common

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
		
    def run(self):
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
            viewer="bin/p-image-viewer"
            #viewer="/home/pi/src/rpi-rgb-led-matrix/utils/p-image-viewer"
        elif self.contentType == "VIEW-VIDEO":
            viewer="bin/p-video-viewer"    
        elif self.contentType == "VIEW-TEXT":
            viewer="bin/p-text-scroller"            

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

