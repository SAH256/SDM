
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


# Single line text input style class



class StyleInput(QtWidgets.QLineEdit):
    
    def __init__(self):
        super().__init__()

        self.setAutoFillBackground(True)
        self.setClearButtonEnabled(True)

        self.prop_name = 'cssClass'
        self.class_name = 'double'


    # set double border property
    def set_double(self, state):
        name = ''
        if state:
            name = self.class_name
        
        self.setProperty(self.prop_name, name)

    def setObjectName(self, name):
        super().setObjectName(name)

        self.style().polish(self)
        self.style().unpolish(self)

    
    def _reset(self):
        self.setText('')



