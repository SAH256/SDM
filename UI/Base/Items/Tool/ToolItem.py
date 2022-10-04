from PyQt5 import QtWidgets, QtGui

from ..BaseItem import BaseItem

# Tool item UI class for action item like add, resume, ...



class ToolItem(BaseItem):

    def __init__(self, parent, icon_name):
        super().__init__(parent)

        self.base_icon = icon_name

        self._normal = '-normal.png'
        self._hover = '-hover.png'
        self._size = 32

        layout = self.mainLayout.itemAt(0)
        layout.setContentsMargins(0, 0, 0, 0)

        name = 'tool-item'
        self.setObjectName(name)
        


    def _toggle_icon(self, normal = True):
        name = self.path_name + self.base_icon

        if normal:
            name += self._normal
        else:
            name += self._hover
        
        pixmap = self.get_pixmap(name)

        if pixmap:
            self.set_icon(pixmap)
    

    def get_pixmap(self, key):
        super().get_pixmap()

        pixmap = self.cache.find(key)

        if not pixmap:
            icon = QtGui.QIcon(key)
            if not icon.isNull():
                pixmap = icon.pixmap(self._size, self._size)
                self.cache.insert(key, pixmap)
        
        return pixmap


    def setDisabled(self, s):
        super().setDisabled(s)

        d = 1

        if s:
            d = 0.4
            
        self._toggle_icon(s)
        # self.set_opacity(d)

    def setEnabled(self, s):
        super().setEnabled(s)

        d = 0.4
        if s:
            d = 1

        if self.entered:
            self._toggle_icon(not s)

        # self.set_opacity(d)

    # def set_opacity(self, value):
    #     self.iconPlace.graphicsEffect().setOpacity(value)

    def enterEvent(self, ev):
        super().enterEvent(ev)

        self.entered = True

        if self.isEnabled():
            self._toggle_icon(False)
        
    def leaveEvent(self, ev):
        super().leaveEvent(ev)
            
        self.entered = False

        if self.isEnabled():
            self._toggle_icon()


