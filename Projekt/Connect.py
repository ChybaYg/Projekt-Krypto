import socket
import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator, QPixmap
from PyQt5.QtWidgets import QMessageBox

import Client
from Client import connectionClient
import Login



class Ui_connectWindow(object):
    def setupUi(self, connectWindow):
        connectWindow.setWindowIcon(QtGui.QIcon('favicon.png'))
        connectWindow.setObjectName("connectWindow")
        connectWindow.setFixedSize(466, 230)
        connectWindow.setStyleSheet("background-color: black;")
        connectWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(connectWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 40, 371, 151))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.adressLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.adressLabel.setFont(font)
        self.adressLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.adressLabel.setObjectName("adressLabel")
        self.adressLabel.setStyleSheet("QLabel{ color: white}")
        self.verticalLayout.addWidget(self.adressLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addressLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.addressLine.setStyleSheet("Address")
        self.addressLine.setText("")
        self.addressLine.setFrame(True)
        self.addressLine.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.addressLine.setPlaceholderText("Address")
        self.addressLine.setObjectName("addressLine")
        self.addressLine.setInputMask("000.000.000.000")
        self.addressLine.setStyleSheet("QLineEdit{background-color: rgb(128, 128, 128); color: white}")
        self.horizontalLayout.addWidget(self.addressLine)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.portLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.portLine.setMaximumSize(QtCore.QSize(80, 16777215))
        self.portLine.setFrame(True)
        self.portLine.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.portLine.setObjectName("portLine")
        self.portLine.setMaxLength(5)

        self.portLine.setStyleSheet("QLineEdit{background-color: rgb(128, 128, 128); color: white}")
        portRegex = QRegularExpression("(?:[0-5]?[0-9]?[0-9]?[0-9]?[0-9]|6[0-5][0-5][0-3][0-6])")
        portValidator = QRegularExpressionValidator(portRegex)
        self.portLine.setValidator(portValidator)

        self.horizontalLayout.addWidget(self.portLine)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.connectButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setBold(True)
        font.setWeight(75)
        self.connectButton.setFont(font)
        self.connectButton.setObjectName("connectButton")
        self.connectButton.setStyleSheet("QPushButton{background-color: rgb(128, 128, 128); color: white}")
        self.connectButton.setDefault(True)
        self.verticalLayout.addWidget(self.connectButton)
        self.connectButton.clicked.connect(lambda: self.connectToStorage())
        self.connectButton.clicked.connect(lambda: self.hideWindow())
        self.exitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setBold(True)
        font.setWeight(75)
        self.exitButton.setFont(font)
        self.exitButton.setObjectName("exitButton")
        self.exitButton.setStyleSheet("QPushButton{background-color: rgb(128, 128, 128); color: white}")
        self.exitButton.setDefault(True)
        self.exitButton.clicked.connect(lambda: connectWindow.close())
        self.verticalLayout.addWidget(self.exitButton)
        connectWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(connectWindow)
        self.statusbar.setObjectName("statusbar")
        connectWindow.setStatusBar(self.statusbar)

        self.retranslateUi(connectWindow)
        QtCore.QMetaObject.connectSlotsByName(connectWindow)

    def retranslateUi(self, connectWindow):
        _translate = QtCore.QCoreApplication.translate
        connectWindow.setWindowTitle(_translate("connectWindow", "Establishment of a connection"))
        self.adressLabel.setText(_translate("connectWindow", "Enter IP address and port of randezvous server"))
        self.label_2.setText(_translate("connectWindow", ":"))
        self.portLine.setPlaceholderText(_translate("connectWindow", "Port"))
        self.connectButton.setText(_translate("connectWindow", "Connect"))
        self.exitButton.setText(_translate("connectWindow", "Exit"))

    def connectToStorage(self):
        import ipaddress
        ip_string = self.addressLine.text()
        port_string = self.portLine.text()
        if not port_string:
            self.warningBox()
        else:
            ipaddress.ip_address(ip_string)

            self.connect = Client.connectionClient()
            self.connect.connection(self.addressLine.text(), int(self.portLine.text()))

            self.MainWindow = QtWidgets.QMainWindow()
            self.ui = Login.Ui_loginWindow()
            self.ui.setupUi(self.MainWindow)
            self.MainWindow.show()
            #self.connect.sendMess()
            self.exitButton.click()

    def hideWindow(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)
        self.MainWindow.hide()

    def warningBox(self):
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setBold(True)
        font.setWeight(600)
        font.setPointSize(11)
        msg = QMessageBox()
        msg.setWindowIcon(QtGui.QIcon('favicon.png'))
        msg.setStyleSheet("background-color: black; color: white")
        msg.setFont(font)
        msg.setWindowTitle("Error!")
        msg.setText("IP address or port is not valid!")
        msg.setIcon(QMessageBox.Warning)
        msg.setDefaultButton(QtWidgets.QPushButton())
        msg.exec_()
