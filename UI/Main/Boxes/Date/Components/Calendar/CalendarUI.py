
from PyQt5 import QtWidgets
# import resource

from UI.Base.Input.StyledInput import StyleInput
from UI.Base.Button.StyledButton import StyleButton

from Utility.Core import ICONS


class CalendarUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self._combo()
        self._btn()

        self.mainLayout.addStretch(1)
    

    def _combo(self):
        comboLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(comboLayout, 4)

        self.dateCombo = StyleInput()
        self.dateCombo.setClearButtonEnabled(False)

        comboLayout.addWidget(self.dateCombo)

    def _btn(self):
        btnLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(btnLayout)

        self.calBtn = StyleButton(ICONS.OTHER.CALENDAR, '')
        self.calBtn.icon_selector(True)

        btnLayout.addWidget(self.calBtn)

















