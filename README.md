#TempController
####Arduino Temperature Controller

##Dependencies
**Python 2.7**

**PyQt5**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;http://pyqt.sourceforge.net/Docs/PyQt5/installation.html

**matplotlib:**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sudo apt-get install python-dev python-pip libfreetype6-dev qt5-default pyqt5-dev-tools
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pip install matplotlib

**Serial Communications:**

You may need to run:
`sudo chmod 666 /dev/ttyUSB0`
`sudo usermod -aG dialout \`whoami\``
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;in order to communicate with the Arduino

##How to upload to Arduino
run `sudo arduino` in terminal and open Arduino/Arduino.ino file

####Upload settings
**Dependencies**
sudo apt-get install arduino arduino-core

**Board:** Arduino Pro or Pro Mini (5V, 16MHz) w/ ATmega328

**Serial Port:** /dev/ttyUSB0 (On Ubuntu)

**Programmer:** Arduino as ISP

##How to compile QT
**Run the following Command:** 
pyuic5 tempcontroller.ui > ui_tempcontroller.py

**Note:** You may need to install pyuic5
sudo apt-get install pyuic5

