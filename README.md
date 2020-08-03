# rpi-panel-controller
The Raspberry Pi panel controller is the client part of IoT panel advertising project.
Actually it has just a CLI to control the device.

-------------------

## Requirement
Before start using this, please follow this instruction:
1. download the project hzeller/rpi-rgb-led-matrix :
https://github.com/hzeller/rpi-rgb-led-matrix/
This is the open source driver for matrix panels.
2. Compile it as explained in the README file, using the Makefile provided in the folder */externs*.
3. Switch off on-board sound (dtparam=audio=off in */boot/config.txt*). More detail in the mentioned README file.
4. in the folder *utils/*
```
sudo apt-get update
sudo apt-get install libgraphicsmagick++-dev libwebp-dev -y
sudo apt-get install libmagick++-dev
sudo apt-get install libavcodec-dev
make 
```

## Execution
- The project is based on Python3.
- The main file of the project is *controller.py* and should be executed as sudo.

## User terminal commands 
- There is a second start point for this product in order to use for local tests *controller_local.py*. It should be executed as sudo as well.
```
q/quit     : Quit the program
h/help     : Show help
di/d-image : Display the current file as an image
dv/d-video : Display the current file as a video
dt/d-text  : Display the scrolling text from file
s/stop     : Stop displaying
r/restart  : Display from the beginning
f/file     : set file name
k/killall  : kill all other running viewers
c/showconf : Show current configurations
rc/reloadconf : Reload configuration file
```

## Logging
The log file will generated in the folder */logs* in separated files by date.

## Configuration
There is two config file provided in the project:
#### *matrix.cfg*
  This file includes all configurations related to the the viewers.
#### *device.cfg*
  This file includes registration information of the device.

