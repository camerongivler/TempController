#TempController
###Arduino Temperature Controller

##Dependencies
**Python 2.7**

**PyQt5**

**matplotlib:**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pip install matplotlib

##How to upload to Arduino
####Upload settings
**Board:** Arduino Pro or Pro Mini (5V, 16MHz) w/ ATmega328

**Serial Port:** /dev/ttyUSB0 (On Ubuntu)

**Programmer:** Arduino as ISP

##How to compile QT
**Run the following Command:** 
pyuic5 tempcontroller.ui > ui_tempcontroller.py

**Note:** You may need to install pyuic5