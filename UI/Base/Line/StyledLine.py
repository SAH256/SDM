
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class Line(QtWidgets.QWidget):
    
    def __init__(self, horizontal = True):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        css_attr = 'orientation'
        value = 'v'
        w, h = 3, 30

        if horizontal:
            value = 'h'
            t = w
            h = w
            w = t
            
        self.setFixedSize(w, h)
        self.setProperty(css_attr, value)


        name = 'line'
        self.setObjectName(name)

