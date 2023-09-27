from PyQt5 import QtWidgets

from PlayerMainWindow import Ui_PlayerMainWindow


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PlayerMainWindow = QtWidgets.QMainWindow()
    ui = Ui_PlayerMainWindow()
    ui.setupUi(PlayerMainWindow)
    PlayerMainWindow.show()
    sys.exit(app.exec_())

