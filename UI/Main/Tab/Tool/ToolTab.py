from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt



class ToolTab(QtWidgets.QWidget):
    
    def __init__(self, parent, direction):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.mainLayout = QtWidgets.QBoxLayout(direction)
        self.setLayout(self.mainLayout)

        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addStretch(1)

        self.items = []
        
        name = 'tool-tab'
        self.setObjectName(name)



