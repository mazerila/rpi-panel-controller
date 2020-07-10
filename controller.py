#!/usr/bin/env python3
import sys
import os
import logging
import configparser
import subprocess
import signal
from threading import Thread
from time import time
#--------------------------------------------------------------
# todo: 
# 1. parse the config file
# 2. object oriented structure for configs
#--------------------------------------------------------------
class MatrixConfig:
	configFile="matrix.cfg"
	displayWidth = 64;
	displayHeight = 32;
	panelCols="64"
	panelRows="32"
	chainLength="1"
	parallelCount="1"
	multiplexing="0"
	slowdownGpio="2"
	pwmLsbN1anoseconds="200"
	brightness="80"
	pixelMapper="Mirror:V;Mirror:H"
	nohardwarePulse=True
	
	def parseConfig(self, filename = configFile):
		
		return
		
class PanelDisplay (Thread):
	proc = None
	filename = "/home/pi/src/samples/vid01.mp4"
	contentType = "VIEW-IMAGE"
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
	def	play(self, cType):
		self.contentType = cType
		self.run()
	def	run(self):
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
		# Default values for parameters
		cols="--led-cols=64"
		rows="--led-rows=32"
		chain="--led-chain=1"
		parallel="--led-parallel=1"
		multiplexing="--led-multiplexing=0"
		slowdown="--led-slowdown-gpio=2"
		pwm="--led-pwm-lsb-nanoseconds=200"
		brightness="--led-brightness=80"
		mapper="--led-pixel-mapper=Mirror:V;Mirror:H"
		nohardware="--led-no-hardware-pulse"
		# os.system("ls -l")

		if self.contentType == "VIEW-IMAGE":
			viewer="/home/pi/src/rpi-rgb-led-matrix/utils/led-image-viewer"
		elif self.contentType == "VIEW-VIDEO":
			viewer="/home/pi/src/rpi-rgb-led-matrix/utils/video-viewer"			

		print (viewer, "Displaying the file: ", self.filename)
		logging.info("Displaying the file: " + self.filename)
		
		cmd_params = list([viewer])
		# TODO : adding other options: -f -w5 -l2 -t10
		cmd_params.extend(["-f -F"])
		cmd_params.extend([cols, rows, chain, parallel, multiplexing, slowdown, pwm, brightness])
		cmd_params.extend([self.filename])
		cmd = " ".join(cmd_params)
		# The os.setsid() is passed in the argument preexec_fn so
		# it's run after the fork() and before  exec() to run the shell.
		self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

		
#--------------------------------------------------------------
# Global vriables


#--------------------------------------------------------------
# General methods

def showHelp():
	print ("---------------------------------------------\n"
		   " q/quit     : Quit the program\n"
		   " h/help     : Show help \n"
	       " di/d-image : Display the current file as an image \n"
	       " dv/d-video : Display the current file as a video \n"
	       " s/stop     : Stop displaying\n"
	       " r/restart  : Display from the beginning\n"
	       " f/file     : set file name \n"
	       " k/killall  : kill all other running viewers \n"
	       "---------------------------------------------\n")
	
def userCommandDict(cmd):
	switcher={
		"h":"HELP",
		"help":"help",
		"q":"QUIT",
		"quit":"QUIT",
		"di":"VIEW-IMAGE",
		"d-image":"VIEW-IMAGE",
		"dv":"VIEW-VIDEO",
		"d-video":"VIEW-VIDEO",
		"r":"RESTART",
		"restart":"RESTART",
		"s":"STOP",
		"stop":"STOP",
		"f":"FILE",
		"file":"FILE",
		"k":"KILLALL",
		"killall":"KILLALL"
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
		logging.info(str(len(pidList))+" running viewer(s) already exist. Killing them before start.")
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
		elif userCommandDict(cmd)== "VIEW-IMAGE":
			th_panel.play(userCommandDict(cmd))
		elif userCommandDict(cmd)== "VIEW-VIDEO":
			th_panel.play(userCommandDict(cmd))
		elif userCommandDict(cmd)== "RESTART":
			th_panel.restart()
		elif userCommandDict(cmd)== "STOP":
			th_panel.terminate()
		elif userCommandDict(cmd)== "FILE":
			th_panel.filename = input("enter the file name: ")
		elif userCommandDict(cmd)== "KILLALL":
			killAll()
	  
	logging.info('Exiting Main Thread : Took %s', time() - ts)
	logging.info('Finished')


if __name__ == '__main__':
	main()
#--------------------------------------------------------------
