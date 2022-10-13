from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from Utility.Structure.Setting import Interface

# Toolbar container for category or action items
class ToolBar(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        name = 'toolbar'
        self.setObjectName(name)


    def add_action(self, action):
        layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(layout)

        layout.addWidget(action)


    def add_space(self, d):
        self.mainLayout.addStretch(d)


