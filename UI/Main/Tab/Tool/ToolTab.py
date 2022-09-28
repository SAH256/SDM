from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt



class ToolTab(QtWidgets.QWidget):
    
    def __init__(self, parent, direction):
        super().__init__()

        self.setAutoFillBackground(True)
        self.__change_color(self.backgroundRole())

        self.mainLayout = QtWidgets.QBoxLayout(direction)
        self.setLayout(self.mainLayout)

        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addStretch(1)


    def __change_color(self, role, color = '#fff'):
        p = self.palette()
        p.setColor(role, QtGui.QColor(color))
        self.setPalette(p)



