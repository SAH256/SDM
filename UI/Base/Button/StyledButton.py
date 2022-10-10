
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from Utility.Core import SELECTORS

# Base Button class for modifying its style and behaviour




class StyleButton(QtWidgets.QPushButton):
    
    def __init__(self, icon, text = None):
        super().__init__(text)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if icon:
            self.setIcon(QtGui.QIcon(icon))



    def set_type(self, _type):
        if _type:
            self.setProperty(SELECTORS.PROPERTY.CSS_CLASS, _type)


    # change style to icon button style
    def icon_selector(self, state):

        if state:
            self.set_type(SELECTORS.VALUE.ICON)
            self.update()
    

    def update(self):
        self.style().unpolish(self)
        self.style().polish(self)
        super().update()


