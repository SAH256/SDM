
from PyQt5 import QtWidgets

from UI.Base.CheckBox.StyledCheckBox import CheckBox

from Utility.Core import WEEK


class WeekUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QGridLayout()
        self.setLayout(self.mainLayout)
        self.widgets = {}

        self._days()

    def _days(self):

        days = [
            'Saturday',
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
        ]

        row = 0
        col = 0
        max_row = 2

        for day in days:
            wid = CheckBox(day)

            self.widgets[WEEK.day_to_index.get(day)] = wid
            self.mainLayout.addWidget(wid, row, col)

            row += 1

            if row == max_row:
                col += 1
                row = 0


    def get_data(self):

        return {key : wid.isChecked() for key, wid in self.widgets.items()}


    def set_data(self, data):

        for index, state in data.items():
            self.widgets[index].setChecked(state)


    def reset(self):
        data = {str(i) : True for i in range(1, 8)}
        self.set_data(data)











