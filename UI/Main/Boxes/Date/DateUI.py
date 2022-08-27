from PyQt5 import QtWidgets

from UI.Base.ComboBox.StyledComboBox import ComboBox

from .Components.Repeat.RepeatUI import RepeatUI
from .Components.Calendar.CalendarControl import CalendarControl
from .Components.Week.WeekUI import WeekUI


# Date select widget -- UI class
class DateUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self._combo()
        self._repeat()
        self._stack()


    def _combo(self):
        comboLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(comboLayout)

        txt = 'Based On : '
        self.optionCombo = ComboBox()

        comboLayout.addWidget(QtWidgets.QLabel(txt))
        comboLayout.addWidget(self.optionCombo, 1)

        comboLayout.addStretch(3)


    def _repeat(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)

        self.repeat = RepeatUI()
        self.repeat.setVisible(False)

        layout.addWidget(self.repeat)


    def _stack(self):
        self.stackLayout = QtWidgets.QStackedLayout()
        self.mainLayout.addLayout(self.stackLayout)

        self.__calender()
        self.__week()


    def __calender(self):
        wid = CalendarControl()
        self.CALENDAR_INDEX = self.stackLayout.addWidget(wid)


    def __week(self):
        wid = WeekUI()
        self.WEEK_INDEX = self.stackLayout.addWidget(wid)

