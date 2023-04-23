import os
import Client
import Login

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QWidget, QFileSystemModel, QTreeWidgetItem, QTreeWidget, QMessageBox

# Inicializace globálních proměnných
global file_choosen,tag_name
file_choosen = ""
tag_name = ""


class MainWindow(QWidget):
    # Metoda definující vzhled okna a funkcionalitu tlačítek
    def setupUi(self, main_window):
        main_window.setWindowIcon(QtGui.QIcon('Icons/favicon.png'))
        main_window.setObjectName("main_window")
        main_window.setFixedSize(899, 545)
        main_window.setStyleSheet("background-color: black")
        self.centralwidget = QtWidgets.QWidget(main_window)
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
        self.tagName = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.tagName.setObjectName("tagName")
        self.tagName.hide()
        self.verticalLayout.addWidget(self.tagName)
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
        self.homeButton.setIcon(QtGui.QIcon('Icons/server-storage.png'))
        self.homeButton.setShortcut(Qt.Key_Return)
        self.verticalLayout.addWidget(self.homeButton)
        self.homeButton.clicked.connect(self.homeScreen)
        self.uploadButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.uploadButton.setFont(font)
        self.uploadButton.setObjectName("uploadButton")
        self.uploadButton.setStyleSheet("QPushButton{background-color: rgb(128, 128, 128); color:white}")
        self.uploadButton.setIcon(QtGui.QIcon('Icons/cloud-computing.png'))
        self.verticalLayout.addWidget(self.uploadButton)
        self.uploadButton.clicked.connect(self.uploadFile)
        self.downloadButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.downloadButton.setFont(font)
        self.downloadButton.setObjectName("downloadButton")
        self.downloadButton.setStyleSheet("QPushButton{background-color: rgb(128, 128, 128); color:white}")
        self.downloadButton.setIcon(QtGui.QIcon('Icons/download.png'))
        self.verticalLayout.addWidget(self.downloadButton)
        self.downloadButton.clicked.connect(self.downloadFile)
        self.deleteButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.deleteButton.setFont(font)
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.clicked.connect(self.deleteFile)
        self.deleteButton.setStyleSheet("QPushButton{background-color: rgb(128, 128, 128); color:white}")
        self.deleteButton.setIcon(QtGui.QIcon('Icons/delete.png'))
        self.verticalLayout.addWidget(self.deleteButton)
        if tag_name == "Admin":
            self.verifyLogsButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
            font = QtGui.QFont()
            font.setFamily("Cascadia Code")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.verifyLogsButton.setFont(font)
            self.verifyLogsButton.setObjectName("uploadButton")
            self.verifyLogsButton.setStyleSheet("QPushButton{background-color: rgb(128, 128, 128); color:white}")
            self.verifyLogsButton.setIcon(QtGui.QIcon('Icons/cloud-computing.png'))
            self.verticalLayout.addWidget(self.verifyLogsButton)
            self.verifyLogsButton.clicked.connect(self.verifyLogsFile)
            self.verifyLogsButton.setText("VERIFY LOGS")
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
        self.infoButton.setIcon(QtGui.QIcon('Icons/info.png'))
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
        self.signOutButton.clicked.connect(lambda: main_window.close())
        self.signOutButton.setIcon(QtGui.QIcon('Icons/logout.png'))
        self.verticalLayout.addWidget(self.signOutButton)
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    # Nastavení titulků
    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Application"))
        self.label.setText(_translate("main_window", "MENU"))
        self.homeButton.setText(_translate("main_window", "HOME"))
        self.downloadButton.setText(_translate("main_window", "DOWNLOAD"))
        self.deleteButton.setText(_translate("main_window", "DELETE FILE"))
        self.infoButton.setText(_translate("main_window", "ABOUT"))
        self.signOutButton.setText(_translate("main_window", "SIGN OUT"))
        self.uploadButton.setText(_translate("main_window", "UPLOAD"))

    # Metoda, která otevře okno k zadání přihlašovacích údajů do uložiště
    def loginWindow(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Login.LoginWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()
        # Reset proměnných
        Client.storage_dictionary = {}
        Client.warning_message = ""
        Client.authenticated_access = ""

    # Metoda pro nahrání souboru
    def uploadFile(self):
        # Otevře okno pro výběr souboru a uloží cestu k souboru do proměnné
        upload_file_path, _ = QFileDialog.getOpenFileName(self, "Upload file", "", "TXT Files (*.txt)")
        if upload_file_path:
            file_size = os.path.getsize(upload_file_path)      # Zjištění velikosti souboru
            if file_size > 65000:        # Pokud je soubor větší jak 65kB, otevře se okno s varováním
                warning = "Cannot be uploaded"
                self.warningBox(warning)
            elif not upload_file_path == "" and file_size < 65000:
                file_name = os.path.basename(upload_file_path)     # Zjištění jména souboru
                self.connect = Client.ConnectionClient()
                with open(upload_file_path, 'rb') as f:     # Načtení a uložení dat souboru do proměnné
                    file = f.read()
                    data = file.decode()
                # Odeslání souboru na uložiště, spolu s jménem uživatele, jménem souboru, daty souboru
                self.connect.uploadFile(self.tagName.text(), file_name, data)
        else:
            pass

    # Metoda pro stažení souboru
    def downloadFile(self):
        if file_choosen == "":      # Kontrola, zda je vybraný některý z souborů
            self.warningBox(file_choosen)
        elif file_choosen.endswith(".txt"):     # Kontrola, že je vybrán soubor a ne složka
            # Otevře nové okno pro výběr místa a jména souboru
            download_file_path = QFileDialog.getSaveFileName(self, "Download file", "", "TXT Files (*.txt)")
            if not download_file_path[0] == "":
                self.connect = Client.ConnectionClient()
                self.connect.getPathDownloadedFile(download_file_path[0])
                # Odeslání požadavku spolu s jménem uživatele a který soubor má být stažen
                self.connect.downloadFile(self.tagName.text(), file_choosen)

    # Metoda pro smazání souboru
    def deleteFile(self):
        result = self.warningBox(file_choosen)  # Otevře okno k potvrzení smazání souboru
        if result == "YES":
            self.connect = Client.ConnectionClient()
            # Odešle příkaz ke smazání souboru spolu se jménem uživatele a vybraného souboru, jenž má být smazán
            self.connect.deleteFile(self.tagName.text(), file_choosen)

    # Metoda pro ověření záznamů
    def verifyLogsFile(self):
        self.connect = Client.ConnectionClient()
        while self.connect.returnLogsInfo() == "":
            self.connect.verifyLogs()
        if self.connect.returnLogsInfo() != "":
            info = self.connect.returnLogsInfo()        # Získání informace o tom, zda jsou shodné či nikoli
            self.warningBox(info)       # Zobrazení okna s výsledkem ověření
            Client.verification_logs = ""       # Reset proměnné

    # Metoda pro zobrazení obsahu uložiště
    def homeScreen(self):
        global file_choosen
        file_choosen = ""
        self.clearLayout()
        self.connect = Client.ConnectionClient()
        self.connect.getStorage(self.tagName.text())
        self.tree = QTreeWidget()
        self.frame = QFileSystemModel()
        self.tree.setHeaderLabel("STORAGE")
        while self.connect.getStorageFull() == {}:
            self.connect.getStorage(self.tagName.text())
        # Získání proměnné jenž předává slovník, ve kterém je uložený seznam souborů
        storage = self.connect.getStorageFull()
        # Výpis všech souborů, které jsou v uložišti
        for key, value in storage.items():
            root = QTreeWidgetItem(self.tree, [key])
            for val in value:
                item = QTreeWidgetItem([val])
                root.addChild(item)
        self.tree.expandAll()
        self.tree.setColumnWidth(0, 250)
        self.tree.setAlternatingRowColors(True)
        self.tree.setStyleSheet("background-color: rgb(192,192,192);")
        self.verticalLayout_2.addWidget(self.tree)
        self.tree.itemClicked.connect(self.onClicked)

    # Metoda, která do proměnné ukládá název souboru, na který bylo kliknuto
    def onClicked(self, item, column):
        global file_choosen
        file_choosen = item.text(column)

    # Metoda zobrazující informace o uložišti
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
        self.frameInfo.setText("About us\nThis project is beta version of secured storage.\nUnstable version v1.0")
        self.verticalLayout_2.addWidget(self.frameInfo)

    # Metoda, která vymaže obsah zobrazeného okna
    def clearLayout(self):
        while self.verticalLayout_2.count():
            child = self.verticalLayout_2.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # Metoda definující, jak bude vypadat "pop-up" okno, které se zobrazuje při různých operacích
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
        msg.setWindowTitle("Confirm operation!")
        # Na základě předávaných informací se určuje, jaký text bude v okně zobrazen
        if action == "":
            msg.setWindowTitle("Confirm operation!")
            msg.setText(f"Choose file!")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif action == "Cannot be uploaded":
            msg.setWindowTitle("Warning!")
            msg.setText(f"File is too large!")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif action == "Same" or action== "Different":
            msg.setWindowTitle("Information!")
            msg.setText(f"Logs are {action}!")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            msg.setWindowTitle("Confirm operation!")
            msg.setText(f"Do you really want delete this file:\n{action}")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            result = msg.exec_()
            if result == QMessageBox.Yes:
                return "YES"
            elif result == QMessageBox.No:
                return "NO"
