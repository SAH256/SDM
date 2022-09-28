
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

# Base Button class for modifying its style and behaviour




class StyleButton(QtWidgets.QPushButton):
    
    def __init__(self, icon, text):
        super().__init__(text)

        if icon:
            self.setIcon(QtGui.QIcon(icon))

        self.prop_name = 'css-class'
        self.icon_prop = 'icon'

        self.setCursor(Qt.CursorShape.PointingHandCursor)


    def set_type(self, _type):
        if _type:
            self.setProperty(self.prop_name, _type)

    # assigning style SELECTOR
    def set_selector(self, name):
        self.setObjectName(name)

    # change style to icon button style
    def icon_selector(self, state):
        name = ''

        if state:
            name = self.icon_prop
        
        if name:
            self.setProperty(self.prop_name, name)
            self.update()
    

    def update(self):
        self.style().unpolish(self)
        self.style().polish(self)
        super().update()


