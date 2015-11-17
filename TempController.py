#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, random, Queue, matplotlib, threading, time, csv, serial, smtplib
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

        self.tempChart = MyMplCanvas(self.ui.frame_2, 10, 10)
        self.ui.verticalLayout_2.addWidget(self.tempChart)

        self.humidityChart = MyMplCanvas(self.ui.frame_2, 10, 10)
        self.ui.verticalLayout_5.addWidget(self.humidityChart)

        self.serialManager = SerialManager(self.updateTempChart, self.updateHumidityChart)

        self.requestDataTimer = QtCore.QTimer()
        self.requestDataTimer.timeout.connect(self.requestData)
        self.requestDataTimer.start(5000)

        self.connect_signals()

        self.tempData = []
        self.tempTimes = []
        self.humidityData = []
        self.humidityTimes = []

        self.alerted = False
        self.turnedOff = False
        self.alertHum = float('Inf')

    @pyqtSlot()
    def set_temperature(self):
        print "Temperature:", self.ui.tempSpinBox.value()
        self.serialManager.setTemp(self.ui.tempSpinBox.value())

    @pyqtSlot()
    def set_warning_humidity(self):
        print "Alert Humidity:", self.ui.warningThresholdSpinBox.value()
        self.alertHum = self.ui.warningThresholdSpinBox.value()

    @pyqtSlot()
    def set_turn_off_humidity(self):
        print "Turn off Humidity:", self.ui.turnOffThresholdSpinBox.value()
        self.serialManager.setHumidity(self.ui.turnOffThresholdSpinBox.value())

    @pyqtSlot()
    def connect_to_arduino(self):
        self.ui.connectButton.disconnect()
        self.ui.connectButton.clicked.connect(self.disconnect_from_arduino)
        self.ui.connectButton.setText("Disconnect")
        self.ui.ConnectField.setDisabled(True)
        serialLocation = self.ui.ConnectField.text()
        if not serialLocation:
            serialLocation = "/dev/ttyUSB0"
        print "Connect to:", serialLocation
        self.serialManager.connect(serialLocation);

    @pyqtSlot()
    def disconnect_from_arduino(self):
        if(self.serialManager):
            self.serialManager.endSerial()
        self.ui.connectButton.disconnect()
        self.ui.connectButton.clicked.connect(self.connect_to_arduino)
        self.ui.connectButton.setText("Connect")
        self.ui.ConnectField.setDisabled(False)

    @pyqtSlot()
    def exportTempData(self):
        exportLocation = self.ui.tempExportField.text()
        if not exportLocation:
            exportLocation = "tempData.csv"
        self.exportData(self.tempTimes, self.tempData, exportLocation)

    @pyqtSlot()
    def exportHumidityData(self):
        exportLocation = self.ui.humidityExportField.text()
        if not exportLocation:
            exportLocation = "humidityData.csv"
        self.exportData(self.humidityTimes, self.humidityData, exportLocation)

    def exportData(self, times, data, exportLocation):
        print "exporting to:", exportLocation
        with open(exportLocation, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(times)
            writer.writerow(data)

    @pyqtSlot()
    def requestData(self):
        self.serialManager.writeLine("get data")

    @pyqtSlot()
    def addEmail(self):
        email = self.ui.addEmailField.text()
        self.ui.addEmailField.setText("")
        self.ui.emailList.addItem(email)

    @pyqtSlot()
    def deleteEmail(self):x
        listItems=self.ui.emailList.selectedItems()
        for item in listItems:
           self.ui.emailList.takeItem(self.ui.emailList.row(item))

    def connect_signals(self):
        self.ui.tempSetButton.clicked.connect(self.set_temperature)
        self.ui.warningThresholdButton.clicked.connect(self.set_warning_humidity)
        self.ui.turnOffThresholdButton.clicked.connect(self.set_turn_off_humidity)
        self.ui.connectButton.clicked.connect(self.connect_to_arduino)
        self.ui.tempExportButton.clicked.connect(self.exportTempData)
        self.ui.humidityExportButton.clicked.connect(self.exportHumidityData)
        self.ui.addEmailButton.clicked.connect(self.addEmail)
        self.ui.removeEmailButton.clicked.connect(self.deleteEmail)

    def updateTempChart(self, data):
        x = list(self.perdelta(datetime.today(), datetime.today() - timedelta(minutes=(len(data))), timedelta(minutes=1)))
        times = matplotlib.dates.date2num(x)
        self.tempTimes = [time.strftime("%x %X") for time in x]
        self.tempData = data
        self.tempChart.graphData(times, data)

    def updateHumidityChart(self, data):
        x = list(self.perdelta(datetime.today(), datetime.today() - timedelta(minutes=(len(data))), timedelta(minutes=1)))
        times = matplotlib.dates.date2num(x)
        self.humidityTimes = [time.strftime("%x %X") for time in x]
        self.humidityData = data
        self.humidityChart.graphData(times, data)
        if data[0] > self.alertHum and not self.alerted:
            self.alerted = True

    def sendAlert(self):
        print "humidity too high!" #this needs to send an email
        reply = QMessageBox.question(self, 'Warning',
                    "Humidity too high", QMessageBox.Ok)
        self.alerted = False

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
    def __init__(self, updateTempChart, updateHumChart):
        self.timer = QtCore.QTimer()
        self.queue = Queue.Queue()
        self.ser = None
        self.running = False
        self.thread = None
        self.updateTempChart = updateTempChart
        self.updateHumChart = updateHumChart

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
            if msg == "temperatures":
                self.updateTempChart(getArray())
            if msg == "humidities":
                self.updateHumChart(getArray())

        if not self.running:
            self.timer.stop()
            self.timer.timeout.disconnect()

    def setTemp(self, num):
        self.writeLine("setTemp")
        self.writeLine(str(num))

    def setHumidity(self, num):
        self.writeLine("setMaxHumidity")
        self.writeLine(str(num))

    def getArray(self):
        while not self.queue.qsize() and self.running: # wait until the data arrives
            time.sleep(0.01)
        try:
            return self.queue.get(0).split(",")
        except Queue.Empty:
            return null

    def writeLine(self, msg):
        if self.ser:
            self.ser.write(msg + "\r\n")

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
