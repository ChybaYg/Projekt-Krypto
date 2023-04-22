from PyQt5 import QtWidgets

from Connect import ConnectWindow

# Spuštění aplikace
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    connectWindow = QtWidgets.QMainWindow()
    ui = ConnectWindow()
    ui.setupUi(connectWindow)
    connectWindow.show()
    sys.exit(app.exec_())
