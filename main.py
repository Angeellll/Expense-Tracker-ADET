from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('progress1.ui', self)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # BUTTON
        self.start.clicked.connect(self.progress)
        self.n = 101
        self.count = 0

    # PROGRESS BAR
    def progress(self):
        for i in range(101):
            self.count += 1
            QtCore.QThread.msleep(10)
            self.progressBar.setValue(self.count)
        if self.count >= self.n:
            msg = QMessageBox.question(self, 'Loading Succesfully', 'Do you want to proceed?',
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                       )
            if msg == QMessageBox.StandardButton.Yes:
                QMessageBox.information(
                    self,
                    'Information',
                    'You selected Yes. You may now go to the next form.',
                    QMessageBox.StandardButton.Ok
                )
                self.myApp = MyApp()
                self.myApp.show()
                self.hide()

            else:
                QMessageBox.information(
                    self,
                    'Information',
                    'You selected No. This program will be terminated',
                    QMessageBox.StandardButton.Ok
                )


class MyApp(QMainWindow):
    def __init__(self, parent = None):
        super(MyApp,self).__init__(parent)
        loadUi('mainscreen.ui', self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())

