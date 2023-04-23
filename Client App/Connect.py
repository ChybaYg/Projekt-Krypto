import Client
import Login

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator, QPixmap
from PyQt5.QtWidgets import QMessageBox


class ConnectWindow(object):
    # Definice vzhledu okna a funkcionality tlačítek
    def setupUi(self, connect_window):
        connect_window.setWindowIcon(QtGui.QIcon('Icons/favicon.png'))
        connect_window.setObjectName("connect_window")
        connect_window.setFixedSize(466, 230)
        connect_window.setStyleSheet("background-color: black;")
        connect_window.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(connect_window)
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

        # Nastavení, že zadávaný port bude v platném rozsahu
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
        self.exitButton.clicked.connect(lambda: connect_window.close())
        self.verticalLayout.addWidget(self.exitButton)
        connect_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(connect_window)
        self.statusbar.setObjectName("statusbar")
        connect_window.setStatusBar(self.statusbar)

        self.retranslateUi(connect_window)
        QtCore.QMetaObject.connectSlotsByName(connect_window)

    # Nastavení titulků
    def retranslateUi(self, connectWindow):
        _translate = QtCore.QCoreApplication.translate
        connectWindow.setWindowTitle(_translate("connect_window", "Establishment of a connection"))
        self.adressLabel.setText(_translate("connect_window", "Enter IP address and port of randezvous server"))
        self.label_2.setText(_translate("connect_window", ":"))
        self.portLine.setPlaceholderText(_translate("connect_window", "Port"))
        self.connectButton.setText(_translate("connect_window", "Connect"))
        self.exitButton.setText(_translate("connect_window", "Exit"))

    # Metoda připojující aplikaci k serveru, potažmo k uložišti
    def connectToStorage(self):
        import ipaddress
        ip_string = self.addressLine.text()
        port_string = self.portLine.text()
        # Kontrola, že je zadaná ip_address adresa a port
        if not port_string or not ip_string:
            self.warningBox()       # Zobrazení varování, v případě, že není zadaná ip_address adresa nebo port
        else:
            ipaddress.ip_address(ip_string)     # Kontrola, že ip_address adresa je v platném rozsahu
            # Ustanovení spojení na dané ip_address adrese a portu
            self.connect = Client.ConnectionClient()
            self.connect.connection(self.addressLine.text(), int(self.portLine.text()))
            # Zobrazení přihlašovacího okna
            self.MainWindow = QtWidgets.QMainWindow()
            self.ui = Login.LoginWindow()
            self.ui.setupUi(self.MainWindow)
            self.MainWindow.show()
            self.exitButton.click()

    # Metoda skrývající okno, pokud by toto okno bylo zavřeno, celá aplikace by se zavřela
    def hideWindow(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)
        self.MainWindow.hide()

    # Definice vzhledu "pop-up" okna
    def warningBox(self):
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setBold(True)
        font.setWeight(600)
        font.setPointSize(11)
        msg = QMessageBox()
        msg.setWindowIcon(QtGui.QIcon('Icons/favicon.png'))
        msg.setStyleSheet("background-color: black; color: white")
        msg.setFont(font)
        msg.setWindowTitle("Error!")
        msg.setText("IP address or port is not valid!")
        msg.setIcon(QMessageBox.Warning)
        msg.setDefaultButton(QtWidgets.QPushButton())
        msg.exec_()
