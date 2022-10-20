
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from Utility.Structure.Setting import Interface
from Utility.Core import COLOR_ROLE

# Base widget for containing process sub sections
class Base(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self._title()
        self._content()

        name = 'process-container'
        self.setObjectName(name)


    def _add_shadow(self):
        e = QtWidgets.QGraphicsDropShadowEffect()
        e.setColor(QtGui.QColor(Interface.COLORS.get(COLOR_ROLE.CONTAINER_SHADOW)))
        e.setOffset(0, 0)
        e.setBlurRadius(10)

        self.setGraphicsEffect(e)


    def _title(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 5, 0, 10)
        self.mainLayout.addLayout(layout)

        self.title = QtWidgets.QLabel()
        layout.addWidget(self.title)

        name = 'container-title'
        self.title.setObjectName(name)


    def _content(self):
        self.conLayout = QtWidgets.QVBoxLayout()
        self.conLayout.setContentsMargins(10, 0, 0, 5)
        self.mainLayout.addLayout(self.conLayout)


    def set_title(self, txt):
        if txt and isinstance(txt, str):
            self.title.setText(txt)

