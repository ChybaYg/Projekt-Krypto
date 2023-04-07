import json
import os
import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget, QFileSystemModel, QTreeView, QTreeWidgetItem, QTreeWidget

import Client
import Login


class Ui_mainWindow(QWidget):
    def setupUi(self, mainWindow):
        global path
        path = ""
        mainWindow.setWindowIcon(QtGui.QIcon('favicon.png'))
        mainWindow.setObjectName("mainWindow")
        mainWindow.setFixedSize(899, 545)
        mainWindow.setStyleSheet("background-color: black")
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(160, 50, 711, 461))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 50, 131, 461))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setStyleSheet("QLabel{color:white}")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.homeButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.homeButton.setFont(font)
        self.homeButton.setCheckable(False)
        self.homeButton.setAutoDefault(False)
        self.homeButton.setDefault(False)
        self.homeButton.setFlat(False)
        self.homeButton.setObjectName("homeButton")
        self.homeButton.setStyleSheet("QPushButton{background-color: rgb(128, 128, 128); color:white}")
        self.homeButton.setIcon(QtGui.QIcon('server-storage.png'))

        self.homeButton.clicked.connect(self.homeScreen)
        self.homeButton.clicked.connect(self.homeScreen)

        self.verticalLayout.addWidget(self.homeButton)
        self.uploadButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.uploadButton.setFont(font)
        self.uploadButton.setObjectName("uploadButton")
        self.uploadButton.clicked.connect(self.uploadFile)
        self.uploadButton.setStyleSheet("QPushButton{background-color: rgb(128, 128, 128); color:white}")
        self.uploadButton.setIcon(QtGui.QIcon('cloud-computing.png'))
        self.verticalLayout.addWidget(self.uploadButton)
        self.downloadButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.downloadButton.setFont(font)
        self.downloadButton.setObjectName("downloadButton")
        self.downloadButton.clicked.connect(self.downloadFile)
        self.downloadButton.setStyleSheet("QPushButton{background-color: rgb(128, 128, 128); color:white}")
        self.downloadButton.setIcon(QtGui.QIcon('download.png'))
        self.verticalLayout.addWidget(self.downloadButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.infoButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.infoButton.setFont(font)
        self.infoButton.setObjectName("infoButton")
        self.infoButton.clicked.connect(self.showInfo)
        self.infoButton.setStyleSheet("QPushButton{background-color: rgb(128, 128, 128); color:white}")
        self.infoButton.setIcon(QtGui.QIcon('info.png'))
        self.verticalLayout.addWidget(self.infoButton)
        self.signOutButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.signOutButton.setFont(font)
        self.signOutButton.setStyleSheet("QPushButton{background-color: rgb(128, 128, 128); color:white}")
        self.signOutButton.setObjectName("signOutButton")
        self.signOutButton.clicked.connect(self.loginWindow)
        self.signOutButton.clicked.connect(lambda: mainWindow.close())
        self.signOutButton.setIcon(QtGui.QIcon('logout.png'))
        self.verticalLayout.addWidget(self.signOutButton)
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Application"))
        self.label.setText(_translate("mainWindow", "MENU"))
        self.homeButton.setText(_translate("mainWindow", "HOME"))
        self.uploadButton.setText(_translate("mainWindow", "UPLOAD"))
        self.downloadButton.setText(_translate("mainWindow", "DOWNLOAD"))
        self.infoButton.setText(_translate("mainWindow", "ABOUT US"))
        self.signOutButton.setText(_translate("mainWindow", "SIGN OUT"))

    def loginWindow(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Login.Ui_loginWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

    def uploadFile(self):
        global pathuploadfile, path
        if not path:
            path = ""
        pathuploadfile = QFileDialog.getOpenFileName(self, "Upload file", path, "All Files (*.*)")
        pathUploadFile = pathuploadfile[0]
        print(pathUploadFile)
        self.connect = Client.connectionClient()
        self.connect.uploadFile(pathUploadFile)

    def downloadFile(self):
        global pathdownloadfile, path
        if not path:
            path = ""
        fileName = os.path.basename(path)
        default_filename = os.path.join("D://", fileName)
        pathdownloadfile = QFileDialog.getSaveFileName(self, "Download file", default_filename, "All Files (*.*)")
        pathdownloadfile = pathdownloadfile[0]
        print(pathdownloadfile)

    def homeScreen(self):
        self.clearLayout()
        self.connect = Client.connectionClient()
        self.connect.getStorage()
        self.tree = QTreeWidget()
        self.frame = QFileSystemModel()
        self.tree.setHeaderLabel("STORAGE")
        storage = self.connect.getStorageFull()
        print(storage)
        for key, value in storage.items():  # TreeList.items():
            root = QTreeWidgetItem(self.tree, [key])
            for val in value:
                item = QTreeWidgetItem([val])
                root.addChild(item)
        self.tree.setColumnWidth(0, 250)
        self.tree.setAlternatingRowColors(True)
        self.tree.setStyleSheet("background-color: rgb(192,192,192);")
        self.verticalLayout_2.addWidget(self.tree)
        self.tree.itemClicked.connect(self.onClicked)

    def onClicked(self, item, column):
        print(f"Item clicked: {item.text(column)}")


    def showInfo(self):
        self.clearLayout()
        self.frameInfo = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.frameInfo.setFont(font)
        self.frameInfo.setStyleSheet("QLabel{color:white}")
        self.frameInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.frameInfo.setObjectName("label")
        self.frameInfo.setText("About us\nTBD")
        self.verticalLayout_2.addWidget(self.frameInfo)

    def clearLayout(self):
        while self.verticalLayout_2.count():
            child = self.verticalLayout_2.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

