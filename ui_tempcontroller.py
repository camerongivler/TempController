# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tempcontroller.ui'
#
# Created: Thu Dec 10 20:37:24 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TempController(object):
    def setupUi(self, TempController):
        TempController.setObjectName("TempController")
        TempController.resize(640, 703)
        TempController.setMinimumSize(QtCore.QSize(0, 0))
        self.horizontalLayout = QtWidgets.QHBoxLayout(TempController)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(TempController)
        self.tabWidget.setObjectName("tabWidget")
        self.setupTab = QtWidgets.QWidget()
        self.setupTab.setObjectName("setupTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.setupTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.groupBox_4 = QtWidgets.QGroupBox(self.setupTab)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ConnectField = QtWidgets.QLineEdit(self.groupBox_4)
        self.ConnectField.setObjectName("ConnectField")
        self.horizontalLayout_4.addWidget(self.ConnectField)
        self.connectButton = QtWidgets.QPushButton(self.groupBox_4)
        self.connectButton.setObjectName("connectButton")
        self.horizontalLayout_4.addWidget(self.connectButton)
        self.verticalLayout_4.addWidget(self.groupBox_4)
        self.groupBox = QtWidgets.QGroupBox(self.setupTab)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.frame_5 = QtWidgets.QFrame(self.groupBox)
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.tempSpinBox = QtWidgets.QDoubleSpinBox(self.frame_5)
        self.tempSpinBox.setObjectName("tempSpinBox")
        self.horizontalLayout_2.addWidget(self.tempSpinBox)
        self.tempSetButton = QtWidgets.QPushButton(self.frame_5)
        self.tempSetButton.setObjectName("tempSetButton")
        self.horizontalLayout_2.addWidget(self.tempSetButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_8.addWidget(self.frame_5)
        self.frame_6 = QtWidgets.QFrame(self.groupBox)
        self.frame_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem3)
        self.tempToleranceSpinBox = QtWidgets.QDoubleSpinBox(self.frame_6)
        self.tempToleranceSpinBox.setObjectName("tempToleranceSpinBox")
        self.horizontalLayout_9.addWidget(self.tempToleranceSpinBox)
        self.tempWarningButton = QtWidgets.QPushButton(self.frame_6)
        self.tempWarningButton.setObjectName("tempWarningButton")
        self.horizontalLayout_9.addWidget(self.tempWarningButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem4)
        self.verticalLayout_8.addWidget(self.frame_6)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.setupTab)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.frame_3 = QtWidgets.QFrame(self.groupBox_3)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem5)
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setObjectName("label")
        self.horizontalLayout_8.addWidget(self.label)
        self.warningThresholdSpinBox = QtWidgets.QDoubleSpinBox(self.frame_3)
        self.warningThresholdSpinBox.setObjectName("warningThresholdSpinBox")
        self.horizontalLayout_8.addWidget(self.warningThresholdSpinBox)
        self.humidityWarningButton = QtWidgets.QPushButton(self.frame_3)
        self.humidityWarningButton.setObjectName("humidityWarningButton")
        self.horizontalLayout_8.addWidget(self.humidityWarningButton)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem6)
        self.verticalLayout_7.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.groupBox_3)
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.label_2 = QtWidgets.QLabel(self.frame_4)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.turnOffThresholdSpinBox = QtWidgets.QDoubleSpinBox(self.frame_4)
        self.turnOffThresholdSpinBox.setObjectName("turnOffThresholdSpinBox")
        self.horizontalLayout_3.addWidget(self.turnOffThresholdSpinBox)
        self.turnOffThresholdButton = QtWidgets.QPushButton(self.frame_4)
        self.turnOffThresholdButton.setObjectName("turnOffThresholdButton")
        self.horizontalLayout_3.addWidget(self.turnOffThresholdButton)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.verticalLayout_7.addWidget(self.frame_4)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.groupBox_7 = QtWidgets.QGroupBox(self.setupTab)
        self.groupBox_7.setObjectName("groupBox_7")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem9)
        self.emailList = QtWidgets.QListWidget(self.groupBox_7)
        self.emailList.setMinimumSize(QtCore.QSize(100, 0))
        self.emailList.setMaximumSize(QtCore.QSize(200, 16777215))
        self.emailList.setObjectName("emailList")
        self.horizontalLayout_7.addWidget(self.emailList)
        self.frame_2 = QtWidgets.QFrame(self.groupBox_7)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem10)
        self.addEmailField = QtWidgets.QLineEdit(self.frame_2)
        self.addEmailField.setInputMask("")
        self.addEmailField.setObjectName("addEmailField")
        self.verticalLayout_6.addWidget(self.addEmailField)
        self.addEmailButton = QtWidgets.QPushButton(self.frame_2)
        self.addEmailButton.setObjectName("addEmailButton")
        self.verticalLayout_6.addWidget(self.addEmailButton)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem11)
        self.removeEmailButton = QtWidgets.QPushButton(self.frame_2)
        self.removeEmailButton.setObjectName("removeEmailButton")
        self.verticalLayout_6.addWidget(self.removeEmailButton)
        self.horizontalLayout_7.addWidget(self.frame_2)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem12)
        self.verticalLayout_4.addWidget(self.groupBox_7)
        spacerItem13 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem13)
        self.tabWidget.addTab(self.setupTab, "")
        self.tempTab = QtWidgets.QWidget()
        self.tempTab.setObjectName("tempTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tempTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem14)
        self.groupBox_5 = QtWidgets.QGroupBox(self.tempTab)
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tempExportField = QtWidgets.QLineEdit(self.groupBox_5)
        self.tempExportField.setObjectName("tempExportField")
        self.horizontalLayout_5.addWidget(self.tempExportField)
        self.tempExportButton = QtWidgets.QPushButton(self.groupBox_5)
        self.tempExportButton.setObjectName("tempExportButton")
        self.horizontalLayout_5.addWidget(self.tempExportButton)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem15)
        self.tabWidget.addTab(self.tempTab, "")
        self.humidityTab = QtWidgets.QWidget()
        self.humidityTab.setObjectName("humidityTab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.humidityTab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem16 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem16)
        self.groupBox_6 = QtWidgets.QGroupBox(self.humidityTab)
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.humidityExportField = QtWidgets.QLineEdit(self.groupBox_6)
        self.humidityExportField.setObjectName("humidityExportField")
        self.horizontalLayout_6.addWidget(self.humidityExportField)
        self.humidityExportButton = QtWidgets.QPushButton(self.groupBox_6)
        self.humidityExportButton.setObjectName("humidityExportButton")
        self.horizontalLayout_6.addWidget(self.humidityExportButton)
        self.verticalLayout_5.addWidget(self.groupBox_6)
        spacerItem17 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem17)
        self.tabWidget.addTab(self.humidityTab, "")
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(TempController)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TempController)

    def retranslateUi(self, TempController):
        _translate = QtCore.QCoreApplication.translate
        TempController.setWindowTitle(_translate("TempController", "Temperature Controller"))
        self.groupBox_4.setTitle(_translate("TempController", "Connect To Arduino"))
        self.ConnectField.setPlaceholderText(_translate("TempController", "/dev/ttyUSB0"))
        self.connectButton.setText(_translate("TempController", "Connect"))
        self.groupBox.setTitle(_translate("TempController", "Temperature Setpoint"))
        self.tempSetButton.setText(_translate("TempController", "Set Temperature"))
        self.tempWarningButton.setText(_translate("TempController", "Set Temperature Tolerance"))
        self.groupBox_3.setTitle(_translate("TempController", "Humidity Thresholds"))
        self.label.setText(_translate("TempController", "Warning:"))
        self.humidityWarningButton.setText(_translate("TempController", "Set Threshold"))
        self.label_2.setText(_translate("TempController", "Turn off Cooler:"))
        self.turnOffThresholdButton.setText(_translate("TempController", "Set Threshold"))
        self.groupBox_7.setTitle(_translate("TempController", "Emails"))
        self.addEmailField.setPlaceholderText(_translate("TempController", "email address"))
        self.addEmailButton.setText(_translate("TempController", "Add Email"))
        self.removeEmailButton.setText(_translate("TempController", "Remove Email"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.setupTab), _translate("TempController", "Setup"))
        self.groupBox_5.setTitle(_translate("TempController", "Export Data"))
        self.tempExportField.setPlaceholderText(_translate("TempController", "tempData.csv"))
        self.tempExportButton.setText(_translate("TempController", "Export"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tempTab), _translate("TempController", "Temperature"))
        self.groupBox_6.setTitle(_translate("TempController", "Export Data"))
        self.humidityExportField.setPlaceholderText(_translate("TempController", "humidityData.csv"))
        self.humidityExportButton.setText(_translate("TempController", "Export"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.humidityTab), _translate("TempController", "Humidity"))

