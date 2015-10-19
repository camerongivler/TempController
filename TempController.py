#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
import Queue
import matplotlib
import threading
import time
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ui_tempcontroller import Ui_TempController

import serial


class TempController(QWidget):
    def __init__(self, parent=None):
        super(TempController, self).__init__(parent)
        self.ui = Ui_TempController()
        self.ui.setupUi(self)
        self.serialManager = SerialManager()

        dc = MyStaticMplCanvas(self.ui.frame_2)
        self.ui.verticalLayout_2.addWidget(dc)

        self.connect_signals()

    @pyqtSlot()
    def set_temperature(self):
        print "Temperature:", self.ui.TempSpinBox.value()

    @pyqtSlot()
    def set_humidity(self):
        print "Humidity:", self.ui.HumiditySpinBox.value()

    @pyqtSlot()
    def connect_to_arduino(self):
        serialLocation = self.ui.ConnectField.text()
        if not serialLocation:
            serialLocation = "/dev/ttyUSB0"
        print "Connect to:", serialLocation
        self.serialManager.connect(serialLocation);

    def connect_signals(self):
        self.ui.TempSetButton.clicked.connect(self.set_temperature)
        self.ui.HumiditySetButton.clicked.connect(self.set_humidity)
        self.ui.connectButton.clicked.connect(self.connect_to_arduino)

    def closeEvent(self, event):
        if(self.serialManager):
            self.serialManager.endSerial()

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)

class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]

        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class SerialManager:
    def __init__(self):
        self.timer = QtCore.QTimer()
        self.queue = Queue.Queue()
        self.ser = None
        self.running = False
        self.thread = None

    def connect(self, location):
        if(self.ser or self.running or (self.thread and self.thread.isAlive())):
            self.endSerial()

        try:
            self.ser = serial.Serial(location, 9600, timeout=0.5)
        except:
            print "Could not open serial:", location
            return False

        self.timer.timeout.connect(self.periodicCall)
        self.timer.start(100)

        self.running = True
        self.thread = threading.Thread(target=self.workerThread)
        self.thread.start()

        self.writeLine("get data")

        return True

    def periodicCall(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                print msg.split(",")
            except Queue.Empty: pass

        if not self.running:
            self.timer.stop()
            self.timer.timeout.disconnect()

    def writeLine(self, msg):
        self.ser.write(msg + "\r\n")

    def endSerial(self):
        self.running = False
        self.thread.join()
        self.thread = None

    def workerThread(self):
        while self.running:
            msg = self.ser.readline()
            if (msg):
                self.queue.put(msg.rstrip())
            else: pass
            time.sleep(0.1)
        self.ser.close()
        self.ser = None

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    controller = TempController()
    controller.show()
    sys.exit(app.exec_())
