# rpi-panel-controller
The Raspberry Pi panel controller is the client part of IoT panel advertising project.
Actually it has just a CLI to control the device.

-------------------
<br>

## Requirements
Before start using this, please follow this instruction:
1. download the project *hzeller/rpi-rgb-led-matrix* :
https://github.com/hzeller/rpi-rgb-led-matrix/
This is the open source driver for matrix panels.
2. Compile it as explained in the README file.
3. Switch off on-board sound (dtparam=audio=off in */boot/config.txt*). More detail in the mentioned README file.
4. Compile APIs in the inner folder *rpi-rgb-led-matrix/utils/*, 
   - Copy the Makefile from  *rpi-panel-controller/externs/*  to  *rpi-rgb-led-matrix/utils/*
   - Compile it using the following commands:
```
sudo apt-get update
sudo apt-get install libgraphicsmagick++-dev libwebp-dev -y
sudo apt-get install libmagick++-dev
sudo apt-get install libavcodec-dev
make all
```
<br>

## Execution
- The project is based on Python3.
- The main file of the project is *controller.py* and should be executed as sudo.
```
sudo python3 controller.py
```
<br>
- There is a second start point for this product in order to use for local tests. It should be executed as sudo as well.
```
sudo python3 controller_local.py
```
```
q/quit      : Quit the program
h/help      : Show help
di/d-image  : Display the current file as an image
dv/d-video  : Display the current file as a video
dt/d-text   : Display the scrolling text from file
s/stop      : Stop displaying
r/restart   : Display from the beginning
f/file      : set file name
k/killall   : kill all other running viewers
c/showconf  : Show current configurations
rc/reloadconf : Reload configuration file
```
<br>

## Configuration
There is two config file provided in the project within the folder *configs/*:
#### **matrix.cfg**
  This file includes all configurations related to the the viewers.
#### **device.cfg**
  This file includes registration information of the device.
<br>

## Logging
The log files will generated in the folder *logs/* in separated files by date.

