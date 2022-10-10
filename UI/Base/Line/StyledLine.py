
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from Utility.Core import SELECTORS

class Line(QtWidgets.QWidget):
    
    def __init__(self, horizontal = True):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        value = SELECTORS.VALUE.VERTICAL
        w, h = 3, 30

        if horizontal:
            value = SELECTORS.VALUE.HORIZONTAL
            t = w
            h = w
            w = t
            
        self.setFixedSize(w, h)
        self.setProperty(SELECTORS.PROPERTY.ORIENTATION, value)


        name = 'line'
        self.setObjectName(name)

