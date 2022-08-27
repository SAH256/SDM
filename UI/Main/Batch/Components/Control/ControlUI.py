
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from UI.Base.ComboBox.StyledComboBox import ComboBox
from UI.Base.SpinBox.StyleSpinBoxControl import SpinBoxControl
from UI.Base.Input.StyledInput import StyleInput


# Batch dialog, replacement control -- Control class
class ControlUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom)
        self.setLayout(self.mainLayout)

        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self._options()
        self._stack()


    def _options(self):
        self.optionLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.optionLayout)

        self.__label()
        self.__combo()


    def __label(self):
        text = 'Replace with : '
        label = QtWidgets.QLabel(text)

        self.optionLayout.addWidget(label)
        

    def __combo(self):
        item = ('Number', 'Letter')
        self.optionCombo = ComboBox()
        self.optionCombo.addItems(item)

        self.optionLayout.addWidget(self.optionCombo)
        self.optionLayout.setStretchFactor(self.optionCombo, 2)


    def _stack(self):
        self.stackLayout = QtWidgets.QStackedLayout()
        self.mainLayout.addLayout(self.stackLayout)

        self.__number()
        self.__letter()


    def __number(self):
        wid = QtWidgets.QWidget()
        self.NUMBER_INDEX = self.stackLayout.addWidget(wid)

        layout = QtWidgets.QHBoxLayout()
        wid.setLayout(layout)

        boxes = [
            ('startBox', 'Start',0, 10**5, 0),
            (None, 1),
            ('stopBox', 'End', 0, 10**5, 10),
            (None, 4),
            ('cardBox', 'Wildcard', 1, 12, 1),
        ]

        for item in boxes:
            if item[0]:
                temp = QtWidgets.QHBoxLayout()
                layout.addLayout(temp)

                label = QtWidgets.QLabel(item[1])
                wid = SpinBoxControl(item[4], item[2], item[3])

                temp.addWidget(label)
                temp.addWidget(wid)

                setattr(self, item[0], wid)

            else:
                layout.addStretch(item[1])


    def __letter(self):
        wid = QtWidgets.QWidget()
        self.LETTER_INDEX = self.stackLayout.addWidget(wid)

        layout = QtWidgets.QHBoxLayout()
        wid.setLayout(layout)


        inputs = [
            ('firstChar', 'a'),
            ('lastChar', 'z')
        ]

        for item in inputs:
            temp = QtWidgets.QHBoxLayout()
            layout.addLayout(temp)

            wid = StyleInput()
            wid.setText(item[1])
            wid.setMaxLength(1)

            temp.addWidget(wid, 0, Qt.AlignmentFlag.AlignCenter)

            setattr(self, item[0], wid)

