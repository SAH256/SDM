from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from ..BaseItem import BaseItem
from .ToolItem import ToolItem


# Round Item class for tab secions in scheduler and torrent setting



class RoundItem(ToolItem):

    def __init__(self, icon_name):
        super().__init__(icon_name)

        self.entered = False

        w = 58
        self.setFixedSize(w, w)

        name = 'item'
        self.setObjectName(name)

        self._toggle_icon()
        self.__apply_style()
        
        

    def set_select(self, state):
        super().set_select(state)

        name = ''
        r = 10
        if state:
            r = 0
            name = self.select_value

        self.setProperty(self.css_prop, name)
        self.graphicsEffect().setBlurRadius(r)
        self._toggle_icon()
        self.setFocus()
        self.__apply_style()


    def _effect(self):
        e = QtWidgets.QGraphicsDropShadowEffect()
        e.setColor(Qt.GlobalColor.gray)
        e.setBlurRadius(10)
        e.setOffset(0, 0)
        self.setGraphicsEffect(e)

    def enterEvent(self, ev):
        self.entered = True
        self.graphicsEffect().setColor(Qt.GlobalColor.blue)
        self._toggle_icon()

    def leaveEvent(self, ev):
        self.entered = False
        self.graphicsEffect().setColor(Qt.GlobalColor.gray)
        self._toggle_icon()


    def _toggle_icon(self):
        name = self.path_name + self.base_icon

        if self.selected or self.entered:
            name += self._hover
        else:
            name += self._normal
        
        pixmap = self.get_pixmap(name)
        self.set_icon(pixmap)



    def __apply_style(self):
        style = '''
        #item {
            background-color : white;
            border : 2px solid lightgray;
            border-radius : 29px;
        }

        #item:hover {
            border : 2px solid #3263f3;
        }

        #item[css-class="selected"],
        #item:focus {
            border : 2px solid blue;
            background-color : #eef;
        }

        '''

        self.setStyleSheet(style)


