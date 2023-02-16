from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


# PROGRESS BAR
def progress():
    global count
    for i in range(101):
        count += 1
        QtCore.QThread.msleep(10)
        window.progressBar.setValue(count)
    if count >= n:
        msg = QMessageBox.question(window, 'Loading Successfully', 'Do you want to proceed?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                   )
        if msg == QMessageBox.StandardButton.Yes:
            QMessageBox.information(
                window,
                'Information',
                'You selected Yes. You may now go to the next form.',
                QMessageBox.StandardButton.Ok
            )
            user_selected_yes = True
        else:
            QMessageBox.information(
                window,
                'Information',
                'You selected No. This program will be terminated',
                QMessageBox.StandardButton.Ok
            )
            user_selected_yes = False

    if user_selected_yes:
        import expense_tracker
        expense_tracker.show()
        window.hide()

app = QtWidgets.QApplication(sys.argv)

window = QMainWindow()
loadUi('progress1.ui', window)
window.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
window.setWindowFlags(QtCore.Qt.FramelessWindowHint)

# BUTTON
window.start.clicked.connect(progress)
n = 101
count = 0

myWin = window
myWin.show()
sys.exit(app.exec_())

