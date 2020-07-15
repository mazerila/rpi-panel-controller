# rpi-panel-controller
The Raspberry Pi panel controller is the client part of IoT panel advertising project.

-------------------

### Requirement
Before start using this, please follow this instruction:
1. download the project hzeller/rpi-rgb-led-matrix :
https://github.com/hzeller/rpi-rgb-led-matrix/
This is the open source driver for matrix panels.
2. Compile it as explained in the README file.
3. Switch off on-board sound (dtparam=audio=off in /boot/config.txt). More detail in the mentioned README file.
4. in the folder utils/
```
sudo apt-get update
sudo apt-get install libgraphicsmagick++-dev libwebp-dev -y
sudo apt-get install libmagick++-dev
sudo apt-get install libavcodec-dev
make 
```

### Execution
- The project is based on Python3, however with some tiny modifications you may execute it with python 2 as well.
- This should be executed as sudo

### User terminal commands 
```
q/quit     : Quit the program
h/help     : Show help
di/d-image : Display the current file as an image
dv/d-video : Display the current file as a video
s/stop     : Stop displaying
r/restart  : Display from the beginning
f/file     : set file name
k/killall  : kill all other running viewers
```

### Logging
The log file will generated in the same folder.
