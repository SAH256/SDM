
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

import datetime as dt


class Popup(QtWidgets.QDialog):

    def __init__(self, date = None):
        super().__init__()

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)


        self._calendar(date)

    def _calendar(self, date):
        
        self.calendar = QtWidgets.QCalendarWidget()
        self.calendar.setMinimumDate(dt.date.today())

        if date:
            self.calendar.setSelectedDate(date)

        self.mainLayout.addWidget(self.calendar)


        self.calendar.selectionChanged.connect(self.close)










    def mouseDoubleClickEvent(self, ev):
        super().mouseDoubleClickEvent(ev)

        self.close()
    
    def exec(self):
        super().exec()

        return self.calendar.selectedDate().toPyDate()






