from PyQt5 import QtWidgets, QtGui

from ..BaseItem import BaseItem

# Tool item UI class for action item like add, resume, ...



class ToolItem(BaseItem):

    def __init__(self, parent, icon_name):
        super().__init__(parent)

        self.base_icon = icon_name
        self.__enabled = True

        self._normal = '-normal.svg'
        self._hover = '-hover.svg'
        self._disabled = '-disabled.svg'
        self._size = 32

        layout = self.mainLayout.itemAt(0)
        layout.setContentsMargins(0, 0, 0, 0)

        name = 'tool-item'
        self.setObjectName(name)
        


    def _toggle_icon(self, normal = True):
        name = self.base_icon

        if not self.__enabled:
            name += self._disabled
        elif normal:
            name += self._normal
        else:
            name += self._hover
        
        pixmap = self.get_pixmap(name, self._size)

        if pixmap:
            self.set_icon(pixmap)


    def setDisabled(self, s):
        
        if self.__enabled != (not s):
            self.__enabled = not s
            self._toggle_icon(not s)


    def setEnabled(self, s):

        if self.__enabled != s:
            self.__enabled = s
            self._toggle_icon(s)


    def enterEvent(self, ev):
        super().enterEvent(ev)
        self._check_icon_state()


    def leaveEvent(self, ev):
        super().leaveEvent(ev)
        self._check_icon_state()
            


    def _check_icon_state(self):
        
        if self.__enabled:
            self._toggle_icon(not self.entered)

