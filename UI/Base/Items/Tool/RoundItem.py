from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from Utility.Structure.Setting import Interface
from Utility.Core import SELECTORS, COLOR_ROLE

from ..BaseItem import BaseItem
from .ToolItem import ToolItem


# Round Item class for tab secions in scheduler and torrent setting



class RoundItem(ToolItem):

    def __init__(self, parent, icon_name):
        super().__init__(parent, icon_name)
        
        w = 58
        self.setFixedSize(w, w)

        self._normal = '-normal.png'
        self._hover = '-hover.png'

        self._check_icon_state()
        self._effect()

        name = 'round-item'
        self.setObjectName(name)


    def set_select(self, state):
        super().set_selected(state)

        name = ''
        if state:
            name = SELECTORS.VALUE.SELECTED

        self.setProperty(SELECTORS.PROPERTY.CSS_CLASS, name)
        self._check_icon_state()
        self.update()



    def _effect(self):
        e = QtWidgets.QGraphicsDropShadowEffect()
        e.setBlurRadius(10)
        e.setOffset(0, 0)
        self.setGraphicsEffect(e)
        self.__change_shadow()

    def enterEvent(self, ev):
        super().enterEvent(ev)
        self.__change_shadow(False)


    def leaveEvent(self, ev):
        super().leaveEvent(ev)
        self.__change_shadow()


    def _check_icon_state(self):
        if self.is_selected():
            self._toggle_icon(False)
        else:
            self._toggle_icon(not self.entered)


    def _refresh(self):
        self.__change_shadow()


    def __change_shadow(self, normal = True):
        color_code = Interface.COLORS.get(COLOR_ROLE.ITEM_HOVER_SHADOW)

        if normal:
            color_code = Interface.COLORS.get(COLOR_ROLE.ITEM_NORMAL_SHADOW)

        color = QtGui.QColor(color_code)

        self.graphicsEffect().setColor(color)


    def update(self):
        self.style().unpolish(self)
        self.style().polish(self)
        super().update()
