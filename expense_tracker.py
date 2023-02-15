import sys

from PyQt5.QtCore import QSize, QDate, Qt, QTimer, QTime
from PyQt5.QtGui import QCursor, QIcon, QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFrame, QTextEdit, QDateEdit, QPushButton, QScrollArea, \
    QScrollBar, QMessageBox, QTreeView
import matplotlib.pyplot as plt
import sqlite3
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

# DATABASE CONFIG
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, price DECIMAL, purchase_date TEXT)''')

conn.commit()

# CLEAR FUNCTION
def clearBtn_command():
    expense_item_text.clear()
    item_price_text.clear()

# UPDATE FUNCTION
def updateBtn_command(id):

    if not item_price_text.toPlainText().isnumeric():
        QMessageBox.critical(None, "Error", "Please enter a valid number")
        clearBtn_command()
        return

    item = expense_item_text.toPlainText()
    price = float(item_price_text.toPlainText())
    Date = dateEdit.date().toPyDate().strftime('%Y-%m-%d')

    if item == "" or price == "" or Date == "":
        QMessageBox.critical(None, "Error", "Please fill all the fields")
        return

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE expenses SET item=?, price=?, purchase_date=? WHERE id = ?", (item, price, Date, id))
    conn.commit()
    conn.close()

    QMessageBox.information(None, 'Success', 'Data updated to database successfully!')
    display_data()
    clearBtn_command()

# DISPLAY CHART
def displayChart(window):

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('SELECT item, price FROM expenses')
    data = cursor.fetchall()

    item_totals = {}
    for item, price in data:
        if item not in item_totals:
            item_totals[item] = price
        else:
            item_totals[item] += price

    items = list(item_totals.keys())
    prices = list(item_totals.values())

    fig, ax = plt.subplots()
    ax.pie(prices, labels=items, autopct='%1.1f%%', startangle=90)
    ax.set_title('Item Expenses')
    ax.axis('equal')
    # fig.patch.set_facecolor('purple')
    # ax.patch.set_facecolor('purple')

    canvas = FigureCanvasQTAgg(fig)
    canvas.setParent(window)
    canvas.move(650, 80)
    canvas.resize(250, 230)
    canvas.show()

# SAVE FUNCTION
def saveBtn_command():

    if not item_price_text.toPlainText().isnumeric():
        QMessageBox.critical(None, "Error", "Please enter a valid number")
        clearBtn_command()
        return

    item = expense_item_text.toPlainText()
    price = float(item_price_text.toPlainText())
    Date = dateEdit.date().toPyDate().strftime('%Y-%m-%d')


    if item == "" or price == "" or Date == "":
        QMessageBox.critical(None, "Error", "Please fill all the fields")
        return

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO expenses (item, price, purchase_date) VALUES (?,?,?)", (item, price, Date))
    conn.commit()
    conn.close()

    QMessageBox.information(None, 'Success', 'Data saved to database successfully!')
    display_data()
    clearBtn_command()


# DISPLAY ON TREEVIEW FUNCTION
def display_data():

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(['ID', 'Item', 'Price', 'Date'])

    for expense in expenses:
        id = QStandardItem(str(expense[0]))
        item = QStandardItem(expense[1])
        price = QStandardItem(str(expense[2]))
        date = QStandardItem(expense[3])

        model.appendRow([id, item, price, date])

    tree_view = QTreeView(parent=window)
    tree_view.setStyleSheet("""
    QTreeView {
        font-family: 'Cascadia Code';
        font-size: 12px;
        color: white;
    }

    QHeaderView::section {
        background-color: white;
        font-weight: bold;
        color: BLACK;
    }
    """)

    tree_view.setModel(model)
    tree_view.setGeometry(0, 100, 600, 350)
    tree_view.clicked.connect(select_item)
    tree_view.show()

def select_item(index):
    id = index.sibling(index.row(), 0).data()
    item = index.sibling(index.row(), 1).data()
    price = index.sibling(index.row(), 2).data()
    date = index.sibling(index.row(), 3).data()
    expense_item_text.setText(item)
    item_price_text.setText(str(price))

    dateEdit.setDate(QDate.fromString(date, "yyyy-MM-dd"))

    global selected_id
    selected_id = id


# DELETE FUNCTION
def deleteBtn_command(id):
    conn.execute('DELETE FROM expenses WHERE id=?', (id,))
    conn.commit()
    display_data()

# TOTAL AMOUNT
def total_amount_command():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(price) FROM expenses")
    result = cursor.fetchone()[0]

    if result is None:
        totalamount_2.setText("0.00")
    else:
        totalamount_2.setText("{:.2f}".format(result))

    conn.close()

# TO GET CURRENT DATE
current_date = QDate.currentDate()


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Expense Tracker")
window.resize(949, 618)
window.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0.176136, stop:0 rgba(35, 33, 56, 255), stop:1 rgba(162, 127, 190, 255));")

# FRAME
frame = QFrame(parent=window)
frame.setGeometry(0, 0, 951, 61)
frame.setStyleSheet("background-color: rgb(29, 29, 48);\n"
"border: none;\n"
"")
frame.setFrameShape(QFrame.StyledPanel)
frame.setFrameShadow(QFrame.Raised)
frame.setObjectName("frame")

# HEADER
header = QLabel(parent=window)
header.setText("EXPENSE TRACKER")
header.setGeometry(310, 10, 331, 31)
header.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 20pt \"Cascadia Code\";")
header.setObjectName("header")

# SEPARATOR
line = QFrame(parent=window)
line.setGeometry(600, 60, 5, 561)
line.setMaximumSize(QSize(5, 16777215))
line.setStyleSheet("background-color: rgb(0, 0, 0);")
line.setFrameShape(QFrame.VLine)
line.setFrameShadow(QFrame.Sunken)
line.setObjectName("line")

# EXPENSE LABEL
expense = QLabel(parent=window)
expense.setText("Expense items:")
expense.setGeometry(10, 490, 171, 31)
expense.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Myanmar Text\";")
expense.setObjectName("expense")

# ITEM PRICE LABEL
item_price = QLabel(parent=window)
item_price.setText("Item Price:")
item_price.setGeometry(10, 530, 171, 31)
item_price.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Myanmar Text\";")
item_price.setObjectName("item_price")


# PURCHASE DATE LABEL
purchase_date = QLabel(parent=window)
purchase_date.setText("Purchase Date:")
purchase_date.setGeometry(10, 570, 171, 31)
purchase_date.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Myanmar Text\";")
purchase_date.setObjectName("purchase_date")

# EXPENSE ITEM TEXT BOX
expense_item_text = QTextEdit(parent=window)
expense_item_text.setGeometry(150, 490, 201, 31)
expense_item_text.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))
expense_item_text.setStyleSheet("background-color: rgb(243, 243, 243);\n"
"font: 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
expense_item_text.setObjectName("expense_text")

# ITEM PRICE TEXT BOX
item_price_text = QTextEdit(parent=window)
item_price_text.setGeometry(150, 530, 201, 31)
item_price_text.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))
item_price_text.setStyleSheet("background-color: rgb(243, 243, 243);\n"
"font: 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
item_price_text.setObjectName("expense_text_2")


# DATE PICKER
dateEdit = QDateEdit(parent=window)
dateEdit.setGeometry(150, 570, 201, 22)
dateEdit.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(29, 29, 48);\n"
"font: 9pt \"MS Shell Dlg 2\";")
dateEdit.setDate(current_date)
dateEdit.setDisplayFormat("MM/dd/yyyy")
dateEdit.setObjectName("dateEdit")

# SAVE BUTTON
save = QPushButton(parent=window)
save.setText("Save")
save.setGeometry(380, 470, 100, 40)
save.setCursor(QCursor(Qt.PointingHandCursor))
save.setStyleSheet("background-color: rgb(76, 0, 39);\n"
"font: 75 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
save.clicked.connect(saveBtn_command)

# SAVE ICON
icon = QIcon()
icon.addPixmap(QPixmap("/Users/ASUS/PycharmProjects/pythonProject/venv/icons/save.png"), QIcon.Normal, QIcon.Off)
save.setIcon(icon)
save.setObjectName("save")


# CLEAR BUTTON
clear = QPushButton(parent=window)
clear.setText("Clear")
clear.setGeometry(380, 520, 100, 40)
clear.setCursor(QCursor(Qt.PointingHandCursor))
clear.setStyleSheet("background-color: rgb(87, 10, 87);\n"
"font: 75 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
clear.clicked.connect(clearBtn_command)


# CLEAR ICON
icon1 = QIcon()
icon1.addPixmap(QPixmap("/Users/ASUS/PycharmProjects/pythonProject/venv/icons/eraser.png"), QIcon.Normal, QIcon.Off)
clear.setIcon(icon1)
clear.setObjectName("Clear")


# EXIT BUTTON
exit = QPushButton(parent=window)
exit.setText("Exit")
exit.setGeometry(380, 570, 100, 40)
exit.setCursor(QCursor(Qt.PointingHandCursor))
exit.setStyleSheet("background-color: rgb(117, 5, 80);\n"
"font: 75 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
exit.clicked.connect(app.quit)


# EXIT ICON
icon2 = QIcon()
icon2.addPixmap(QPixmap("/Users/ASUS/PycharmProjects/pythonProject/venv/icons/error.png"), QIcon.Normal, QIcon.Off)
exit.setIcon(icon2)
exit.setObjectName("exit")

# AMOUNT LABEL
totalamount_2 = QLabel(parent=window)
totalamount_2.setGeometry(820, 320, 171, 31)
totalamount_2.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Cascadia Code\";")
totalamount_2.setObjectName("totalamount_2")


# TOTAL BUTTON
total = QPushButton(parent=window)
total.setText("Total")
total.setGeometry(490, 470, 100, 40)
total.setCursor(QCursor(Qt.PointingHandCursor))
total.setStyleSheet("background-color: rgb(125, 6, 51);\n"
"font: 75 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
total.clicked.connect(total_amount_command)



# TOTAL ICON
icon3 = QIcon()
icon3.addPixmap(QPixmap("/Users/ASUS/PycharmProjects/pythonProject/venv/icons/total.png"), QIcon.Normal, QIcon.Off)
total.setIcon(icon3)
total.setObjectName("total")


# UPDATE BUTTON
update = QPushButton(parent=window)
update.setText("Update")
update.setGeometry(490, 520, 100, 40)
update.setCursor(QCursor(Qt.PointingHandCursor))
update.setStyleSheet("background-color: rgb(199, 44, 65);\n"
"font: 75 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
update.clicked.connect(lambda: updateBtn_command(selected_id))


# UPDATE ICON
icon4 = QIcon()
icon4.addPixmap(QPixmap("/Users/ASUS/PycharmProjects/pythonProject/venv/icons/reload.png"), QIcon.Normal, QIcon.Off)
update.setIcon(icon4)
update.setObjectName("update")


# DELETE BUTTON
delete_2 = QPushButton(parent=window)
delete_2.setText("Delete")
delete_2.setGeometry(490, 570, 100, 40)
delete_2.setCursor(QCursor(Qt.PointingHandCursor))
delete_2.setStyleSheet("background-color: rgb(82, 37, 70);\n"
"font: 75 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
delete_2.clicked.connect(lambda: deleteBtn_command(selected_id))

# DELETE ICON
icon5 = QIcon()
icon5.addPixmap(QPixmap("/Users/ASUS/PycharmProjects/pythonProject/venv/icons/delete.png"), QIcon.Normal, QIcon.Off)
delete_2.setIcon(icon5)
delete_2.setObjectName("delete_2")


# TOTAL AMOUNT LABEL
totalamount = QLabel(parent=window)
totalamount.setText("Total Amount:")
totalamount.setGeometry(660, 320, 171, 31)
totalamount.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Cascadia Code\";")
totalamount.setObjectName("totalamount")






# PRINT BUTTON
print = QPushButton(parent=window)
print.setText("Print")
print.setGeometry(730, 570, 100, 40)
print.setCursor(QCursor(Qt.PointingHandCursor))
print.setStyleSheet("background-color: rgb(29, 29, 48);\n"
"font: 75 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")


# PRINT ICON
icon6 = QIcon()
icon5.addPixmap(QPixmap("/Users/ASUS/PycharmProjects/pythonProject/venv/icons/print.png"), QIcon.Normal, QIcon.Off)
print.setIcon(icon6)
print.setObjectName("print")


# SCROLL
scrollArea = QScrollArea(parent=window)
scrollArea.setGeometry(610, 360, 331, 201)
scrollArea.setStyleSheet("background-color: rgb(164, 183, 196);")
scrollArea.setWidgetResizable(True)
scrollArea.setObjectName("scrollArea")
scrollAreaWidgetContents_2 = QWidget()
scrollAreaWidgetContents_2.setGeometry(0, 0, 329, 199)
scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")


verticalScrollBar = QScrollBar(scrollAreaWidgetContents_2)
verticalScrollBar.setGeometry(310, 5, 16, 191)
verticalScrollBar.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(218, 160, 69);")
verticalScrollBar.setOrientation(Qt.Vertical)
verticalScrollBar.setObjectName("verticalScrollBar")


scrollArea.setWidget(scrollAreaWidgetContents_2)


# DATE LABEL
date = QLabel(parent=window)
date.setText("Date:")
date.setGeometry(40, 70, 51, 31)
date.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 italic 10pt \"MS Sans Serif\";")
date.setObjectName("date")


# TIME LABEL
time = QLabel(parent=window)
time.setText("Time:")
time.setGeometry(450, 70, 51, 31)
time.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 italic 10pt \"MS Sans Serif\";")
time.setObjectName("time")


# SET DATE LABEL
setdate = QLabel(parent=window)
setdate.setText(current_date.toString("MM/dd/yyyy"))
setdate.setGeometry(90, 70, 100, 31)
setdate.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 italic 10pt \"MS Sans Serif\";")
setdate.setObjectName("setdate")


# SET TIME LABEL
settime = QLabel(parent=window)
settime.setGeometry(500, 70, 100, 31)
settime.setStyleSheet("background: transparent;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 italic 10pt \"MS Sans Serif\";")
settime.setObjectName("settime")


timer = QTimer(window)
timer.timeout.connect(lambda: settime.setText(QTime.currentTime().toString("hh:mm:ss ap")))
timer.start(1000)


# TREEVIEW
display_data()
displayChart(window)

window.show()
sys.exit(app.exec_())
