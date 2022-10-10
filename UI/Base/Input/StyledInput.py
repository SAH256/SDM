
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from Utility.Core import SELECTORS

# Single line text input style class



class StyleInput(QtWidgets.QLineEdit):
    
    def __init__(self):
        super().__init__()

        self.setAutoFillBackground(True)
        self.setClearButtonEnabled(True)


    # set double border style property
    def set_double(self, state):
        name = ''
        if state:
            name = SELECTORS.VALUE.DOUBLE
        
        self.setProperty(SELECTORS.PROPERTY.CSS_CLASS, name)


    def update(self):
        self.style().unpolish(self)
        self.style().polish(self)
        super().update()

    
    def _reset(self):
        self.setText('')



