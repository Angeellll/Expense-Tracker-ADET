from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtWidgets import QWidget
import sqlite3
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, price DECIMAL, purchase_date TEXT)''')
conn.commit()

class Ui_MainWindow(QWidget):

    def initUi(self, MainWindow):

        def set_time_label(label):
                current_time = QTime.currentTime().toString(Qt.DefaultLocaleLongDate)
                self.settime.text(current_time)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(949, 618)
        MainWindow.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0.176136, stop:0 rgba(35, 33, 56, 255), stop:1 rgba(162, 127, 190, 255));")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 951, 61))
        self.frame.setStyleSheet("background-color: rgb(29, 29, 48);\n"
"border: none;\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.header = QtWidgets.QLabel(self.frame)
        self.header.setGeometry(QtCore.QRect(350, 10, 331, 31))
        self.header.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 20pt \"Cascadia Code\";")
        self.header.setObjectName("header")


        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(600, 60, 5, 561))
        self.line.setMaximumSize(QtCore.QSize(5, 16777215))
        self.line.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")


        self.expense = QtWidgets.QLabel(self.centralwidget)
        self.expense.setGeometry(QtCore.QRect(10, 490, 171, 31))
        self.expense.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Myanmar Text\";")
        self.expense.setObjectName("expense")


        self.item_price = QtWidgets.QLabel(self.centralwidget)
        self.item_price.setGeometry(QtCore.QRect(10, 530, 171, 31))
        self.item_price.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Myanmar Text\";")
        self.item_price.setObjectName("item_price")


        self.purchase_date = QtWidgets.QLabel(self.centralwidget)
        self.purchase_date.setGeometry(QtCore.QRect(10, 570, 171, 31))
        self.purchase_date.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Myanmar Text\";")
        self.purchase_date.setObjectName("purchase_date")


        self.expense_text = QtWidgets.QTextEdit(self.centralwidget)
        self.expense_text.setGeometry(QtCore.QRect(150, 490, 201, 31))
        self.expense_text.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.expense_text.setStyleSheet("background-color: rgb(243, 243, 243);\n"
"font: 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.expense_text.setObjectName("expense_text")


        self.expense_text_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.expense_text_2.setGeometry(QtCore.QRect(150, 530, 201, 31))
        self.expense_text_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.expense_text_2.setStyleSheet("background-color: rgb(243, 243, 243);\n"
"font: 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.expense_text_2.setObjectName("expense_text_2")


        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(150, 570, 201, 22))
        self.dateEdit.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(29, 29, 48);\n"
"font: 9pt \"MS Shell Dlg 2\";")
        self.dateEdit.setMaximumDate(QtCore.QDate(9999, 12, 30))
        self.dateEdit.setObjectName("dateEdit")


        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setGeometry(QtCore.QRect(380, 470, 100, 40))
        self.save.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save.setStyleSheet("background-color: rgb(76, 0, 39);\n"
"font: 75 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save.setIcon(icon)
        self.save.setObjectName("save")
        self.Clear = QtWidgets.QPushButton(self.centralwidget)
        self.Clear.setGeometry(QtCore.QRect(380, 520, 100, 40))
        self.Clear.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Clear.setStyleSheet("background-color: rgb(87, 10, 87);\n"
"font: 75 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/eraser.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Clear.setIcon(icon1)
        self.Clear.setObjectName("Clear")
        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setGeometry(QtCore.QRect(380, 570, 100, 40))
        self.exit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exit.setStyleSheet("background-color: rgb(117, 5, 80);\n"
"font: 75 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/error.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exit.setIcon(icon2)
        self.exit.setObjectName("exit")


        self.total = QtWidgets.QPushButton(self.centralwidget)
        self.total.setGeometry(QtCore.QRect(490, 470, 100, 40))
        self.total.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.total.setStyleSheet("background-color: rgb(125, 6, 51);\n"
"font: 75 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/total.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.total.setIcon(icon3)
        self.total.setObjectName("total")


        self.update = QtWidgets.QPushButton(self.centralwidget)
        self.update.setGeometry(QtCore.QRect(490, 520, 100, 40))
        self.update.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.update.setStyleSheet("background-color: rgb(199, 44, 65);\n"
"font: 75 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/reload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.update.setIcon(icon4)
        self.update.setObjectName("update")


        self.delete_2 = QtWidgets.QPushButton(self.centralwidget)
        self.delete_2.setGeometry(QtCore.QRect(490, 570, 100, 40))
        self.delete_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.delete_2.setStyleSheet("background-color: rgb(82, 37, 70);\n"
"font: 75 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_2.setIcon(icon5)
        self.delete_2.setObjectName("delete_2")


        self.totalamount = QtWidgets.QLabel(self.centralwidget)
        self.totalamount.setGeometry(QtCore.QRect(660, 320, 171, 31))
        self.totalamount.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Cascadia Code\";")
        self.totalamount.setObjectName("totalamount")
        self.totalamount_2 = QtWidgets.QLabel(self.centralwidget)
        self.totalamount_2.setGeometry(QtCore.QRect(820, 320, 171, 31))
        self.totalamount_2.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Cascadia Code\";")
        self.totalamount_2.setObjectName("totalamount_2")


        self.print = QtWidgets.QPushButton(self.centralwidget)
        self.print.setGeometry(QtCore.QRect(730, 570, 100, 40))
        self.print.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.print.setStyleSheet("background-color: rgb(29, 29, 48);\n"
"font: 75 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.print.setIcon(icon6)
        self.print.setObjectName("print")


        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(610, 360, 331, 201))
        self.scrollArea.setStyleSheet("background-color: rgb(164, 183, 196);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 329, 199))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalScrollBar = QtWidgets.QScrollBar(self.scrollAreaWidgetContents_2)
        self.verticalScrollBar.setGeometry(QtCore.QRect(310, 5, 16, 191))
        self.verticalScrollBar.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(218, 160, 69);")
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)


        self.date = QtWidgets.QLabel(self.centralwidget)
        self.date.setGeometry(QtCore.QRect(40, 70, 51, 31))
        self.date.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 italic 10pt \"MS Sans Serif\";")
        self.date.setObjectName("date")


        self.time = QtWidgets.QLabel(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(450, 70, 51, 31))
        self.time.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 italic 10pt \"MS Sans Serif\";")
        self.time.setObjectName("time")


        self.setdate = QtWidgets.QLabel(self.centralwidget)
        self.setdate.setGeometry(QtCore.QRect(90, 70, 71, 31))
        self.setdate.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 italic 10pt \"MS Sans Serif\";")
        self.setdate.setObjectName("setdate")


        self.settime = QtWidgets.QLabel(self.centralwidget)
        self.settime.setGeometry(QtCore.QRect(500, 70, 71, 31))
        self.settime.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 italic 10pt \"MS Sans Serif\";")
        self.settime.setObjectName("settime")

        self.line.raise_()
        self.expense.raise_()
        self.item_price.raise_()
        self.purchase_date.raise_()
        self.expense_text.raise_()
        self.expense_text_2.raise_()
        self.dateEdit.raise_()
        self.frame.raise_()
        self.save.raise_()
        self.Clear.raise_()
        self.exit.raise_()
        self.total.raise_()
        self.update.raise_()
        self.delete_2.raise_()
        self.totalamount.raise_()
        self.totalamount_2.raise_()
        self.print.raise_()
        self.scrollArea.raise_()
        self.date.raise_()
        self.time.raise_()
        self.setdate.raise_()
        self.settime.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Expense Tracker"))
        self.header.setText(_translate("MainWindow", "EXPENSE TRACKER"))
        self.expense.setText(_translate("MainWindow", "Expense items:"))
        self.item_price.setText(_translate("MainWindow", "Item Price:"))
        self.purchase_date.setText(_translate("MainWindow", "Purchase Date:"))
        self.dateEdit.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd"))
        self.save.setText(_translate("MainWindow", "Save"))
        self.Clear.setText(_translate("MainWindow", "Clear"))
        self.exit.setText(_translate("MainWindow", "Exit"))
        self.total.setText(_translate("MainWindow", "Total"))
        self.update.setText(_translate("MainWindow", "Update"))
        self.delete_2.setText(_translate("MainWindow", "Delete"))
        self.totalamount.setText(_translate("MainWindow", "Total Amount:"))
        self.totalamount_2.setText(_translate("MainWindow", "#####"))
        self.print.setText(_translate("MainWindow", "PRINT"))
        self.date.setText(_translate("MainWindow", "Date:"))
        self.time.setText(_translate("MainWindow", "Time:"))
        self.setdate.setText(_translate("MainWindow", "set_date"))
        self.settime.setText(_translate("MainWindow", ""))


import icons_rc
import images_rc
