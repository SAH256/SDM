
from PyQt5 import QtWidgets

from UI.Base.CheckBox.StyledCheckBox import CheckBox
from UI.Base.SpinBox.StyleSpinBoxControl import SpinBoxControl


class RepeatUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self._check()
        self.mainLayout.addStretch(1)
        self._spins()
        self.mainLayout.addStretch(1)

        self.__connect_slots()

    

    def _check(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout, 1)

        txt = 'Start again every'
        self.onCheck = CheckBox(txt, False)

        layout.addWidget(self.onCheck)


    def _spins(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout, 4)

                

        spins = [
            ('hour', 0, 0, 23),
            None,
            ('min', 10, 0, 59),
        ]

        for item in spins:
            if item:
                wid = SpinBoxControl(*item[1:])
                wid.setEnabled(False)

                layout.addWidget(wid)
                layout.addWidget(QtWidgets.QLabel(item[0]))

                setattr(self, item[0], wid)
            else:
                layout.addStretch(1)

        layout.addStretch(12)


    def __connect_slots(self):
        self.onCheck.toggled.connect(self.__check_handler)
    

    def __check_handler(self, s):
        self.hour.setEnabled(s)
        self.min.setEnabled(s)
    

    def is_checked(self):
        return self.onCheck.isChecked()
    
    def set_check(self, s):
        self.onCheck.setChecked(s)


    def get_data(self):
        return (self.hour.get_value(), self.min.get_value()) if self.is_checked() else None

    def set_data(self, data):
        h, m = 0, 10

        if data:
            h, m = data
        else:
            self.set_check(False)
        
        self.hour.set_value(h)
        self.min.set_value(m)









