from PyQt5 import QtWidgets

from UI.Base.CheckBox.StyledCheckBox import CheckBox
from UI.Base.SpinBox.StyleSpinBoxControl import SpinBoxControl


# Timer mini widget -- UI class
class ChronoUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self._check()
        self.mainLayout.addStretch(1)
        self._spins()


    def _check(self):
        checkLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(checkLayout)

        txt = 'Start At:'
        self.onCheck = CheckBox(txt, False)

        checkLayout.addWidget(self.onCheck)


    def _spins(self):
        spinLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(spinLayout)

        spins = [
            ('hour', 12, 0, 23),
            None,
            ('minute', 0, 0, 59),
            None,
            ('second', 0, 0, 59),
        ]

        for item in spins:

            if item:
                wid = SpinBoxControl(*item[1:])
                wid.set_z_fill(2)
                
                setattr(self, item[0], wid)

            else:
                wid = QtWidgets.QLabel(':')

            wid.setEnabled(False)
            spinLayout.addWidget(wid)




