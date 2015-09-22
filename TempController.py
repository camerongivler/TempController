#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget

from ui_tempcontroller import Ui_TempController

import serial


class TempController(QWidget):
    def __init__(self, parent=None):
        super(TempController, self).__init__(parent)
        self.ui = Ui_TempController()
        serialLocation = '/dev/tty.usbserial'
        try:
            self.ser = serial.Serial(serialLocation, 9600)
        except:
            print("Could not open serial:", serialLocation)

        self.ui.setupUi(self)
        self.connect_signals()

    @pyqtSlot()
    def set_temperature(self):
        print("Temperature:", self.ui.TempSpinBox.value())

    @pyqtSlot()
    def set_humidity(self):
        print("Humidity:", self.ui.HumiditySpinBox.value())

    def connect_signals(self):
        self.ui.TempSetButton.clicked.connect(self.set_temperature)
        self.ui.HumiditySetButton.clicked.connect(self.set_humidity)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    controller = TempController()
    controller.show()
    sys.exit(app.exec_())
