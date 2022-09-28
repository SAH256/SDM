from PyQt5 import QtWidgets, QtGui, QtCore

from UI.Base.Items.BaseItem import FilterItem

# Option Item class for category filter



class OptionItem(FilterItem):
    
    def __init__(self, parent, icon):
        super().__init__(parent)

        self.min_size = 32
        self.big_size = 36

        self._effect()

        pm = self.get_pixmap(self.path_name + icon)
        self.set_icon(pm)


        name = 'option-item'
        self.setObjectName(name)
    

    def _effect(self):
        e = QtWidgets.QGraphicsOpacityEffect()
        e.setOpacity(0.5)
        self.iconPlace.setGraphicsEffect(e)



    def set_select(self, state):
        super().set_select(state)

        op = 1

        if not state:
            op = 0.5
            
        self.iconPlace.graphicsEffect().setOpacity(op)


    def enterEvent(self, ev):
        super().enterEvent(ev)
        
        if self.isEnabled():
            self.iconPlace.graphicsEffect().setOpacity(1)

    def leaveEvent(self, ev):
        super().leaveEvent(ev)
        
        if not self.selected:
            self.iconPlace.graphicsEffect().setOpacity(0.5)


    def get_pixmap(self, key):
        super().get_pixmap()

        icon = QtGui.QIcon(key)
        pixmap = icon.pixmap(self.min_size, self.min_size)
        self.cache.insert(key, pixmap)

        return pixmap


















