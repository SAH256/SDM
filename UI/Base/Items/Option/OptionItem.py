from PyQt5 import QtWidgets, QtGui, QtCore

from UI.Base.Items.BaseItem import FilterItem

# Option Item class for category filter



class OptionItem(FilterItem):
    
    def __init__(self, parent, icon):
        super().__init__(parent)

        self.min_size = 32
        self.__icon_name = icon

        self.set_selected(False)
        self.__change_icon()
    
        name = 'option-item'
        self.setObjectName(name)


    def set_selected(self, state):
        super().set_selected(state)
        self.iconPlace.setEnabled(state)


    def enterEvent(self, ev):
        super().enterEvent(ev)
        self.iconPlace.setEnabled(True)
        

    def leaveEvent(self, ev):
        super().leaveEvent(ev)
        
        if self.selected:
            return

        self.iconPlace.setEnabled(False)


    def __change_icon(self):
        pm = self.get_pixmap(self.__icon_name, self.min_size)
        self.set_icon(pm)
    
    
    def _refresh(self):
        self.__change_icon()
