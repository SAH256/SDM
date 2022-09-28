from PyQt5 import QtWidgets


class CheckBox(QtWidgets.QCheckBox):
    
    def __init__(self, text, default = True):
        super().__init__(text)

        self.default = default

        self._reset()


    def _reset(self):
        self.setChecked(self.default)

        