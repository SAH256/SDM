from PyQt5 import QtWidgets, QtGui, QtCore

from UI.Base.Items.BaseItem import FilterItem

# Option Item class for category filter



class OptionItem(FilterItem):
    
    def __init__(self, parent, icon):
        super().__init__(parent)

        self.min_size = 32
        self.big_size = 36

        name = 'option-item'
        self.setObjectName(name)

        pm = self.get_pixmap(self.path_name + icon)
        self.set_icon(pm)
        
        self.set_select(False)
    

    def set_select(self, state):
        super().set_select(state)

        self.iconPlace.setEnabled(state)


    def enterEvent(self, ev):
        super().enterEvent(ev)
        
        self.iconPlace.setEnabled(True)

    def leaveEvent(self, ev):
        super().leaveEvent(ev)
        
        if self.selected:
            return

        self.iconPlace.setEnabled(False)


    def get_pixmap(self, key):
        super().get_pixmap()

        icon = QtGui.QIcon(key)
        pixmap = icon.pixmap(self.min_size, self.min_size)
        self.cache.insert(key, pixmap)

        return pixmap


















