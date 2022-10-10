from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from Utility.Structure.Setting import Interface
from Utility.Core import SELECTORS

from ..BaseItem import BaseItem
from .ToolItem import ToolItem


# Round Item class for tab secions in scheduler and torrent setting



class RoundItem(ToolItem):

    def __init__(self, parent, icon_name):
        super().__init__(parent, icon_name)

        self.entered = False

        w = 58
        self.setFixedSize(w, w)

        name = 'round-item'
        self.setObjectName(name)

        self._toggle_icon()
        self._effect()
        
        

    def set_select(self, state):
        super().set_selected(state)

        name = ''
        r = 10
        if state:
            r = 0
            name = SELECTORS.VALUE.SELECTED

        self.setProperty(SELECTORS.PROPERTY.CSS_CLASS, name)
        self.graphicsEffect().setBlurRadius(r)
        self._toggle_icon()
        self.setFocus()
        self.update()


    def _effect(self):
        e = QtWidgets.QGraphicsDropShadowEffect()
        e.setColor(QtGui.QColor(Interface.COLORS.get('ITEM-NORMAL-SHADOW')))
        e.setBlurRadius(10)
        e.setOffset(0, 0)
        self.setGraphicsEffect(e)

    def enterEvent(self, ev):
        self.entered = True
        self.graphicsEffect().setColor(QtGui.QColor(Interface.COLORS.get('ITEM-HOVER-SHADOW')))
        self._toggle_icon()

    def leaveEvent(self, ev):
        self.entered = False
        self.graphicsEffect().setColor(QtGui.QColor(Interface.COLORS.get('ITEM-NORMAL-SHADOW')))
        self._toggle_icon()


    def _toggle_icon(self):
        name = self.path_name + self.base_icon

        if self.selected or self.entered:
            name += self._hover
        else:
            name += self._normal
        
        pixmap = self.get_pixmap(name)
        self.set_icon(pixmap)


    def update(self):
        self.style().unpolish(self)
        self.style().polish(self)
        super().update()
