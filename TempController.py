#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
import sys, random, queue, matplotlib, threading, time, csv, serial, smtplib, numpy as np
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

        self.tempChart = MyMplCanvas(self.ui.tempTab, 10, 10, "Temperature reading (°C)")
        self.ui.verticalLayout_2.addWidget(self.tempChart)

        self.humidityChart = MyMplCanvas(self.ui.humidityTab, 10, 10, "Humidity reading (% humidity)")
        self.ui.verticalLayout_5.addWidget(self.humidityChart)

        self.serialManager = SerialManager(self.updateTempChart, self.updateHumChart)

        self.requestDataTimer = QtCore.QTimer()
        self.requestDataTimer.timeout.connect(self.requestData)

        self.connect_signals()

        self.tempData = []
        self.tempTimes = []
        self.humidityData = []
        self.humidityTimes = []

        self.humAlert = False
        self.tempAlert = False
        self.coolingOff = False
        self.alertHum = float('Inf')
        self.turnOffHum = float('Inf')
        self.setTemp = 2.5
        self.alertTemp = float('Inf')

    @pyqtSlot()
    def set_warning_temp(self):
        self.alertTemp = self.ui.tempToleranceSpinBox.value()
        print("Alert Temperature:", self.alertTemp)

    @pyqtSlot()
    def set_temperature(self):
        self.coolingOff = False
        self.setTemp = self.ui.tempSpinBox.value()
        self.serialManager.setTemp(self.setTemp)
        print("Temperature:", self.setTemp)

    @pyqtSlot()
    def set_warning_humidity(self):
        self.alertHum = self.ui.warningThresholdSpinBox.value()
        print("Alert Humidity:", self.alertHum)

    @pyqtSlot()
    def set_turn_off_humidity(self):
        self.turnOffHum = self.ui.turnOffThresholdSpinBox.value()
        print("Turn off Humidity:", self.turnOffHum)

    @pyqtSlot()
    def connect_to_arduino(self):
        self.ui.connectButton.disconnect()
        self.ui.connectButton.clicked.connect(self.disconnect_from_arduino)
        self.ui.connectButton.setText("Disconnect")
        self.ui.ConnectField.setDisabled(True)
        serialLocation = self.ui.ConnectField.text()
        if not serialLocation:
            serialLocation = "/dev/ttyUSB0"
        print("Connect to:", serialLocation)
        self.serialManager.connect(serialLocation)
        self.requestData()
        self.requestDataTimer.start(15000)

    @pyqtSlot()
    def disconnect_from_arduino(self):
        self.requestDataTimer.stop()
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
        print("exporting to:", exportLocation)
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
    def deleteEmail(self):
        listItems=self.ui.emailList.selectedItems()
        for item in listItems:
            self.ui.emailList.takeItem(self.ui.emailList.row(item))

    def connect_signals(self):
        self.ui.tempSetButton.clicked.connect(self.set_temperature)
        self.ui.tempWarningButton.clicked.connect(self.set_warning_temp)
        self.ui.humidityWarningButton.clicked.connect(self.set_warning_humidity)
        self.ui.turnOffThresholdButton.clicked.connect(self.set_turn_off_humidity)
        self.ui.connectButton.clicked.connect(self.connect_to_arduino)
        self.ui.addEmailButton.clicked.connect(self.addEmail)
        self.ui.removeEmailButton.clicked.connect(self.deleteEmail)
        self.ui.tempExportButton.clicked.connect(self.exportTempData)
        self.ui.humidityExportButton.clicked.connect(self.exportHumidityData)

    def updateTempChart(self, data):
        x = list(self.perdelta(datetime.today(), datetime.today() - timedelta(minutes=(len(data))), timedelta(minutes=1)))
        times = matplotlib.dates.date2num(x)
        self.tempTimes = [time.strftime("%x %X") for time in x]
        self.tempData = data
        self.tempChart.graphData(times, data)
        if (data[0] > self.setTemp + self.alertTemp or data[0] < self.setTemp - self.alertTemp) and not self.tempAlert:
            listItems = list(map(lambda it: it.text(), self.ui.emailList.findItems("", QtCore.Qt.MatchContains)))
            self.sendTempAlert(listItems)

    def updateHumChart(self, data):
        x = list(self.perdelta(datetime.today(), datetime.today() - timedelta(minutes=(len(data))), timedelta(minutes=1)))
        times = matplotlib.dates.date2num(x)
        self.humidityTimes = [time.strftime("%x %X") for time in x]
        self.humidityData = data
        self.humidityChart.graphData(times, data)
        if data[0] > self.alertHum and not self.humAlert:
            listItems = list(map(lambda it: it.text(), self.ui.emailList.findItems("", QtCore.Qt.MatchContains)))
            self.sendHumAlert(listItems)
        if data[0] > self.turnOffHum and not self.coolingOff:
            listItems = list(map(lambda it: it.text(), self.ui.emailList.findItems("", QtCore.Qt.MatchContains)))
            self.turnCoolingOff(listItems)

    def sendTempAlert(self, listItems):
        self.tempAlert = True
        print("Temperature out of range")
        self.send_email_to_all(listItems, "MIST ALERT: Laser temperature out of range", "Please check the laser as soon as possible. " +
        "The laser temperature is outside of the specified range.")
        self.createMessageBox("Temperature out of range", self.setTempAlertFalse)

    def sendHumAlert(self, listItems):
        self.humAlert = True
        print("humidity warning")
        self.send_email_to_all(listItems, "MIST ALERT: Laser humidity too high", "Please check the laser as soon as possible. " +
        "The laser has reached its warning humidity and cooling will shut off soon.")
        self.createMessageBox("Humidity too high. Cooler will be turned off soon!", self.setHumAlertFalse)

    def turnCoolingOff(self, listItems):
        self.coolingOff = True
        print("Turning off cooling!")
        self.ui.tempSpinBox.setValue(5)
        self.set_turn_off_humidity()
        self.send_email_to_all(listItems, "MIST ALERT: Laser cooling turned off!", "Please check the laser as soon as possible. " +
        "The laser has reached its maximum humidity and cooling has been shut off.")
        self.createMessageBox("Humidity too high.  Cooler has been turned off!", None)

    def createMessageBox(self, msg, func):
        reply = QMessageBox(self)
        reply.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        reply.setStandardButtons(QMessageBox.Ok)
        reply.setWindowTitle("Warning")
        reply.setIcon(QMessageBox.Warning)
        reply.setText(msg);
        reply.setModal(False);
        if func != None:
            reply.destroyed.connect(func)
        reply.show()
        return reply

    @pyqtSlot()
    def setTempAlertFalse(self):
        self.tempAlert = False

    @pyqtSlot()
    def setHumAlertFalse(self):
        self.humAlert = False

    def closeEvent(self, event):
        if(self.serialManager):
            self.serialManager.endSerial()

    def perdelta(self, start, end, delta):
        curr = start
        while curr > end:
            yield curr
            curr -= delta

    def send_email_to_all(self, listItems, subject, body):
        for item in listItems:
            print(item)
            self.send_email(item, subject, body)

    def send_email(self, recipient, subject, body):
        import smtplib

        gmail_user = 'elroy.jetson.mist@gmail.com'
        gmail_pwd = 'Yb171+Yb171+'
        FROM = gmail_user
        TO = recipient if type(recipient) is list else [recipient]
        SUBJECT = subject
        TEXT = body

        # Prepare actual message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            print('successfully sent email')
        except Exception as e:
            print( "Error failed to send email: %s" % str(e) )

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=1, height=1, label="Temperature reading (°C)", dpi=100):
        fig = Figure(dpi=dpi)
        self.label = label
        self.axes = fig.add_subplot(111)
        self.axes.set_xlabel("Minutes in the past")
        self.axes.set_ylabel(label)
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
        self.axes.set_xlabel("Minutes in the past")
        self.axes.set_ylabel(self.label)
        self.axes.set_ylim([-5, 40])
        self.draw()

class SerialManager:
    def __init__(self, updateTempChart, updateHumChart):
        self.timer = QtCore.QTimer()
        self.queue = queue.Queue()
        self.ser = None
        self.running = False
        self.thread = None
        self.updateTempChart = updateTempChart
        self.updateHumChart = updateHumChart

    def connect(self, location):
        if self.ser or self.running or self.thread:
            self.endSerial()

        try:
            self.ser = serial.Serial(location, 9600, timeout=0.5)
        except:
            print("Could not open serial:", location)
            return False

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
            except queue.Empty: pass
            if msg == 'temperatures':
                self.updateTempChart(self.getArray())
            if msg == 'humidities':
                self.updateHumChart(self.getArray())

        if not self.running:
            self.timer.stop()
            self.timer.timeout.disconnect()

    def setTemp(self, num):
        self.writeLine("setTemp")
        self.writeLine(str(num))

    def getArray(self):
        while not self.queue.qsize() and self.running: # wait until the data arrives
            time.sleep(0.01)
        try:
            return list(map(float, self.queue.get(0).split(",")))
        except queue.Empty:
            return null

    def writeLine(self, msg):
        if self.ser:
            self.ser.write((msg + "\r\n").encode())

    def endSerial(self):
        self.running = False
        if self.thread:
            self.thread.join()
            self.thread = None

    def workerThread(self):
        while self.running:
            msg = self.ser.readline().decode()
            if msg:
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
