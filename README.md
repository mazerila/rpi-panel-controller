# rpi-panel-controller
The Raspberry Pi panel controller is the client part of IoT panel advertising project.

-------------------

## Requirements
### RGB panel driver
If you use a RPI3 or RPI4, executable binary files of the panel's driver are already added to the folder *bin/* and you may skip the following instruction.
Otherwise, please follow this instruction to download and compile it.
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
5. Replace three genetared binaries from  *rpi-rgb-led-matrix/utils/*  to  *rpi-panel-controller/bin/*

### Azure IoT service
We use the Microsoft Azure services as our In order to run this application, you may install microsoft azure iot packages for python as sudo:
```
pip3 list | grep -i azure
sudo pip3 install azure-iot-device
```

### GPS
The current GPS model is **VK-162 GMOUSE G-MOUSE GPS Navigation USB**.
The linux package to read the GPS data is called GPSD.
http://www.catb.org/gpsd/
https://gpsd.gitlab.io/gpsd/index.html
Follow the bellow instruction for installing required packeges.
```
sudo apt-get install gpsd gpsd-clients python-gps
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
vim /lib/systemd/system/gpsd.socket
sudo kilall gpsd
sudo gpsd /dev/ttyACM0 -F /var/run/gpsd.sock
```
#### More information about GPS 
Python codes: https://gist.github.com/Lauszus/5785023#file-gps-py
Google API: https://developers.google.com/maps/documentation/javascript/overview#api_key
NMEA Standard: https://www.gpsworld.com/what-exactly-is-gps-nmea-data/
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

