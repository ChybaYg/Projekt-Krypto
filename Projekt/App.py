from PyQt5 import QtWidgets

from Connect import Ui_connectWindow

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    connectWindow = QtWidgets.QMainWindow()
    ui = Ui_connectWindow()
    ui.setupUi(connectWindow)
    connectWindow.show()
    sys.exit(app.exec_())
