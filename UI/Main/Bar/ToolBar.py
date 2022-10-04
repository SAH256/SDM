from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


# Toolbar container for category or action items
class ToolBar(QtWidgets.QWidget):

    def __init__(self, parent, left = True):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        name = 'toolbar'
        self.setObjectName(name)
        
        self.__shadow(left)


    def add_action(self, action):
        layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(layout)

        layout.addWidget(action)


    def add_space(self, d):
        self.mainLayout.addStretch(d)


    def __shadow(self, left):
        off_x = 3
        e = QtWidgets.QGraphicsDropShadowEffect()
        e.setBlurRadius(7)
        e.setOffset(off_x if left else -off_x, 0)
        e.setColor(Qt.GlobalColor.gray)
        self.setGraphicsEffect(e)


