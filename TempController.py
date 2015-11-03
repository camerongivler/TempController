#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, random, Queue, matplotlib, threading, time, csv, serial
from datetime import datetime, timedelta
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from ui_tempcontroller import Ui_TempController

class TempController(QWidget):
    def __init__(self, parent=None):
        super(TempController, self).__init__(parent)
        self.ui = Ui_TempController()
        self.ui.setupUi(self)
        self.serialManager = SerialManager(self.updateGraph)

        self.requestDataTimer = QtCore.QTimer()
        self.requestDataTimer.timeout.connect(self.requestData)
        self.requestDataTimer.start(5000)

        self.dc = MyMplCanvas(self.ui.frame_2, 10, 10)
        self.ui.verticalLayout_2.addWidget(self.dc)

        self.connect_signals()

        self.currentData = []
        self.currentTimes = []

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

    @pyqtSlot()
    def exportData(self):
        exportLocation = self.ui.exportField.text()
        if not exportLocation:
            exportLocation = "tempData.csv"
        print "exporting to:", exportLocation
        with open(exportLocation, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(self.currentTimes)
            writer.writerow(self.currentData)

    def connect_signals(self):
        self.ui.TempSetButton.clicked.connect(self.set_temperature)
        self.ui.HumiditySetButton.clicked.connect(self.set_humidity)
        self.ui.connectButton.clicked.connect(self.connect_to_arduino)
        self.ui.exportButton.clicked.connect(self.exportData)

    @pyqtSlot()
    def requestData(self):
        self.serialManager.writeLine("get data")

    def updateGraph(self, data):
        #x = range(0, len(data))
        x = list(self.perdelta(datetime.today(), datetime.today() - timedelta(minutes=(len(data))), timedelta(minutes=1)))
        times = matplotlib.dates.date2num(x)
        self.currentTimes = [time.strftime("%x %X") for time in x]
        self.currentData = data
        self.dc.graphData(times, data)

    def closeEvent(self, event):
        if(self.serialManager):
            self.serialManager.endSerial()

    def perdelta(self, start, end, delta):
        curr = start
        while curr > end:
            yield curr
            curr -= delta

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=1, height=1, dpi=100):
        fig = Figure(dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_xlabel("Minutes in the past")
        self.axes.set_ylabel("Voltage reading")
        self.axes.hold(False)
        plt.gcf().subplots_adjust(bottom=0.25)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def graphData(self, x, y):
        self.axes.plot_date(x, y, 'r')
        plt.gcf().autofmt_xdate()
        self.axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%I:%M'))
        self.axes.set_xlabel("Time")
        self.axes.set_ylabel("Voltage reading")
        self.axes.set_ylim([0, 5])
        self.draw()

class SerialManager:
    def __init__(self, updateGraph):
        self.timer = QtCore.QTimer()
        self.queue = Queue.Queue()
        self.ser = None
        self.running = False
        self.thread = None
        self.updateGraph = updateGraph

    def connect(self, location):
        if self.ser or self.running or self.thread:
            self.endSerial()

        #try:
        self.ser = serial.Serial(location, 9600, timeout=0.5)
        #except:
        #    print "Could not open serial:", location
        #    return False

        self.timer.timeout.connect(self.periodicCall)
        self.timer.start(100)

        self.running = True
        self.thread = threading.Thread(target=self.workerThread)
        self.thread.start()

        return True

    @pyqtSlot()
    def periodicCall(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
            except Queue.Empty: pass
            #print msg
            if msg == "data":
                while not self.queue.qsize() and self.running: # wait until the data arrives
                    time.sleep(0.01)
                try:
                    self.getData(self.queue.get(0))
                except Queue.Empty: pass

        if not self.running:
            self.timer.stop()
            self.timer.timeout.disconnect()

    def writeLine(self, msg):
        if self.ser:
            self.ser.write(msg + "\r\n")

    def getData(self, msg):
        self.updateGraph(msg.split(","))

    def endSerial(self):
        self.running = False
        if self.thread:
            self.thread.join()
            self.thread = None

    def workerThread(self):
        while self.running:
            msg = self.ser.readline().rstrip()
            if msg:
                self.queue.put(msg)
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
