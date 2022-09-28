from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt



# Toolbar container for category or action items
class ToolBar(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.white)
        self.setPalette(p)

        self.mainLayout.setContentsMargins(0, 0, 0, 0)

    def add_action(self, action):
        layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(layout)

        layout.addWidget(action)
    
    def add_space(self, d):
        self.mainLayout.addStretch(d)












