import Client
import Main

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class LoginWindow(object):
    # Metoda definující vzhled okna a funkcionalitu tlačítek
    def setupUi(self, login_window):
        login_window.setWindowIcon(QtGui.QIcon('Icons/favicon.png'))
        login_window.setObjectName("login_window")
        login_window.setFixedSize(324, 308)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setBold(True)
        font.setWeight(75)
        login_window.setFont(font)
        login_window.setStyleSheet("background-color: black")
        self.centralwidget = QtWidgets.QWidget(login_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 30, 258, 246))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setStyleSheet("QLabel{color:white}")
        self.verticalLayout.addWidget(self.label)
        self.usernameLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.usernameLine.setStyleSheet("Username")
        self.usernameLine.setText("")
        self.usernameLine.setObjectName("usernameLine")
        self.usernameLine.setStyleSheet("QLineEdit{background-color: rgb(128, 128, 128); color: white}")
        self.verticalLayout.addWidget(self.usernameLine)
        self.passwordLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.passwordLine.setAutoFillBackground(False)
        self.passwordLine.setStyleSheet("Password")
        self.passwordLine.setInputMask("")
        self.passwordLine.setText("")
        self.passwordLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLine.setClearButtonEnabled(False)
        self.passwordLine.setObjectName("passwordLine")
        self.passwordLine.setStyleSheet("QLineEdit{background-color: rgb(128, 128, 128); color: white}")
        self.verticalLayout.addWidget(self.passwordLine)
        spacerItem = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.signInButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.signInButton.setEnabled(True)
        self.signInButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setBold(True)
        font.setWeight(75)
        self.signInButton.setFont(font)
        self.signInButton.setAutoDefault(False)
        self.signInButton.setObjectName("signInButton")
        self.signInButton.clicked.connect(self.userCredentials)
        self.signInButton.setStyleSheet("QPushButton{background-color: rgb(128, 128, 128); color: white}")
        self.signInButton.setDefault(True)
        self.signInButton.clicked.connect(lambda: login_window.close())
        self.verticalLayout.addWidget(self.signInButton)
        self.exitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setBold(True)
        font.setWeight(75)
        self.exitButton.setFont(font)
        self.exitButton.setObjectName("exitButton")
        self.exitButton.setStyleSheet("QPushButton{background-color: rgb(128, 128, 128); color: white}")
        self.exitButton.setDefault(True)
        self.exitButton.clicked.connect(lambda: login_window.close())
        self.exitButton.clicked.connect(self.closeConn)
        self.verticalLayout.addWidget(self.exitButton)
        login_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(login_window)
        self.statusbar.setObjectName("statusbar")
        login_window.setStatusBar(self.statusbar)

        self.retranslateUi(login_window)
        QtCore.QMetaObject.connectSlotsByName(login_window)

    # Nastavení titulků
    def retranslateUi(self, login_window):
        _translate = QtCore.QCoreApplication.translate
        login_window.setWindowTitle(_translate("login_window", "Login"))
        self.label.setText(_translate("login_window", "LOGIN"))
        self.usernameLine.setPlaceholderText(_translate("login_window", "Username"))
        self.passwordLine.setPlaceholderText(_translate("login_window", "Password"))
        self.signInButton.setText(_translate("login_window", "Sign in"))
        self.exitButton.setText(_translate("login_window", "Exit"))

    # Metoda vztahující se k přihlašování do uložiště
    def userCredentials(self):
        user_username = self.usernameLine.text()
        user_password = self.passwordLine.text()
        self.connect = Client.ConnectionClient()
        self.connect.keyExchange()      # Ustanovení klíčů pro šifrování spojení

        # Kontrola, zda je vyplněné jméno a heslo
        if not user_password or not user_username:
            self.warningBox("missing")
            self.newWin()
        else:
            while self.connect.returnAccessInfo() == "":
                self.connect.getAccess(user_username, user_password)
            # Na základě zadaných přihlašovacích údajů je buď uživatel informován o nesprávných údajích
            # nebo je připojen k uložišti
            if self.connect.returnAccessInfo() == "Authenticated":
                Main.tag_name = self.usernameLine.text()
                self.toStorage()
                Client.authenticated_access = ""
            elif self.connect.returnAccessInfo() == "Non-authenticated_access":
                self.warningBox("wrong")
                Client.authenticated_access = ""
                self.newWin()
        Client.authenticated_access = ""

    # Metoda zobrazující okno uložiště
    def toStorage(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Main.MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.tagName.setText(self.usernameLine.text())   # Předání jména uživatele
        self.MainWindow.show()

    # Vytvoření nového přihlašovacího okna
    def newWin(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = LoginWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

    # Definice vzhledu "pop-up" okna a jeho obsahu
    def warningBox(self, action):
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
        msg.setIcon(QMessageBox.Warning)
        msg.setDefaultButton(QtWidgets.QPushButton())
        # na základě předávané hodnoty se rozliší, co má být zobrazeno jako text okna
        if action == "missing":
            msg.setText("Username or password missing!")
        elif action == "wrong":
            msg.setText("Wrong username or password!")
        msg.exec_()

    # Uzavření spojení
    def closeConn(self):
        self.connect = Client.ConnectionClient()
        self.connect.closeConnection()
