#!/usr/bin/env python3
import sys
import os
import signal
import subprocess
import logging
from threading import Thread
from time import time

#--------------------------------------------------------------

class PanelDisplay (Thread):
	proc = None
	def __init__(self, threadID, name):
		Thread.__init__(self)
		self.threadID = threadID
		self.name = name
	def terminate(self): 
		self._running = False
		if self.proc != None:
			print("Stopping")
			output = os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)  # Send the signal to all the process groups
			logging.info(output)
			self.proc = None
	def	play(self):
		self.run()
	def	run(self):
		if self.proc == None:
			self.display();
		else:
			print("The panel is already busy!")
	def restart(self):
		print("Restarting")
		if self.proc != None:
			self.terminate();
		self.display()
	def display(self):
		# Default values for parameters
		cols="--led-cols=64"
		rows="--led-rows=32"
		chain="--led-chain=1"
		parallel="--led-parallel=1"
		multiplexing="--led-multiplexing=0"
		slowdown="--led-slowdown-gpio=2"
		pwm="--led-pwm-lsb-nanoseconds=200"
		brightness="--led-brightness=70"
		mapper="--led-pixel-mapper=Mirror:V;Mirror:H"
		nohardware="--led-no-hardware-pulse"
		# other options: -f -w5 -l2 -t10
		# os.system("ls -l")

		# filename="/home/pi/src/samples/gif02-2.gif"
		filename="/home/pi/src/samples/vid01.mp4"

		print ("Displaying the file: ", filename)
		logging.info("Displaying the file: "+filename)
		cmd_params = ("/home/pi/src/rpi-rgb-led-matrix/utils/video-viewer", "-f", cols, rows, chain, parallel, multiplexing, slowdown, pwm, brightness, filename)
		cmd = " ".join(cmd_params)
		# The os.setsid() is passed in the argument preexec_fn so
		# it's run after the fork() and before  exec() to run the shell.
		self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
							   shell=True, preexec_fn=os.setsid) 
		# output = subprocess.call(["/home/pi/src/rpi-rgb-led-matrix/utils/led-image-viewer", "-l3", cols, rows, chain, parallel, multiplexing, slowdown, pwm, brightness, filename])
		# subprocess.call(["/home/pi/src/rpi-rgb-led-matrix/utils/video-viewer", "-f", cols, rows, chain, parallel, multiplexing, slowdown, pwm, brightness, filename])

		#logging.info("Output result: "+str(output))

	
#--------------------------------------------------------------
# Global vriables
interruptFlag = 0

#--------------------------------------------------------------
# General methods

def showHelp():
	print (" q/quit    : Quit the program\n"
		   " h/help    : Show help \n"
	       " d/display : Display the current file\n"
	       " s/stop    : Stop displaying\n"
	       " r/restart : Display from the beginning\n"
	       "----------------------------------------\n")
	
def userCommandDict(cmd):
	switcher={
		"h":"HELP",
		"help":"help",
		"q":"QUIT",
		"quit":"QUIT",
		"d":"START",
		"display":"START",
		"r":"RESTART",
		"restart":"RESTART",
		"s":"STOP",
		"stop":"STOP"
	}
	return switcher.get(cmd,"Invalid request")
#--------------------------------------------------------------
# Main thread

def main():
	logging.basicConfig(filename='controller.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
			th_panel.terminate()
			break
		elif userCommandDict(cmd)== "START":
			th_panel.play()
		elif userCommandDict(cmd)== "RESTART":
			th_panel.restart()
		elif userCommandDict(cmd)== "STOP":
			th_panel.terminate()
	
	  
	logging.info('Exiting Main Thread : Took %s', time() - ts)
	logging.info('Finished')


if __name__ == '__main__':
	main()
#--------------------------------------------------------------
