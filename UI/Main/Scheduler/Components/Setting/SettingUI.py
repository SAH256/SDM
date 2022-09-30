
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from UI.Base.ComboBox.StyledComboBox import ComboBox
from UI.Base.CheckBox.StyledCheckBox import CheckBox
from UI.Base.SpinBox.StyleSpinBoxControl import SpinBoxControl
from UI.Base.Input.StyledInput import StyleInput

from Utility.Core import QUEUE


# Setting widget in Scheduler for a queue -- UI class
class SettingUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self._input()
        self._combo()
        self._spins()
        self._checks()

        self.mainLayout.addStretch(1)
        
        name = 'queue-setting'
        self.setObjectName(name)


    def _input(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 5, 0, 5)
        self.mainLayout.addLayout(layout)

        txt = 'Name'
        label = QtWidgets.QLabel(txt)
        # label.setObjectName(txt)

        self.name = StyleInput()
        self.name.setReadOnly(True)

        layout.addWidget(label)
        layout.addWidget(self.name)


    def _combo(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 5, 0, 5)
        self.mainLayout.addLayout(layout)

        self.typeOption = ComboBox()
        self.typeOption.addItems(QUEUE.SETTING.TIMER_TYPE.values())

        txt = 'Timer Type'
        label = QtWidgets.QLabel(txt)

        layout.addWidget(label)
        layout.addWidget(self.typeOption)


    def _checks(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 5, 0, 5)
        self.mainLayout.addLayout(layout)

        checks = [
            ('startup', 'Start Queue at startup'),
        ]

        for item in checks:
            if item:
                wid = CheckBox(item[1], False)

                layout.addWidget(wid)

                setattr(self, item[0], wid)


    def _spins(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 5, 0, 5)
        self.mainLayout.addLayout(layout)

        spins = [
            ('concurrent', 'Number of Concurrent Download', (1, 1, 10)),
            ('retry', 'Number of Retry if download failed', (0, 0, 99)),
        ]

        for item in spins:

            temp = QtWidgets.QHBoxLayout()
            layout.addLayout(temp)

            label = QtWidgets.QLabel(item[1])
            wid = SpinBoxControl(*item[2])

            temp.addWidget(label)
            temp.addStretch(1)
            temp.addWidget(wid)

            setattr(self, item[0], wid)



