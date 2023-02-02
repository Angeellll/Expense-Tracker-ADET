from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import QTimer
import datetime

def update_time():
    time_label.setText(datetime.datetime.now().strftime("%I:%M:%S %p"))
    date_label.setText(datetime.datetime.now().strftime("%B %d, %Y"))

app = QApplication([])

time_label = QLabel()
time_label.setText(datetime.datetime.now().strftime("%I:%M:%S %p"))
time_label.show()

date_label = QLabel()
date_label.setText(datetime.datetime.now().strftime("%B %d, %Y"))
date_label.move(0, 30)
date_label.show()

timer = QTimer()
timer.timeout.connect(update_time)
timer.start(1000)



app.exec_()
