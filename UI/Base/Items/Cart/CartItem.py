from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from UI.Base.Items.BaseItem import FilterItem


# Header Item Class for queue and status filter



class CartItem(FilterItem):
    
    def __init__(self, parent, icon, name):
        super().__init__(parent)

        self._name(name)
        self.__icon_name = icon
        self.__icon_size = 20

        self.__change_icon()

        txt = 'cart-item'
        self.setObjectName(txt)


    def _name(self, name):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 0, 0, 0)
        self.mainLayout.addLayout(layout)
        
        txt = 'cart-name'
        self.name = QtWidgets.QLabel(name)
        self.name.setObjectName(txt)

        layout.addWidget(self.name)
            

    def get_name(self):
        return self.name.text()


    def update(self):
        self.style().unpolish(self.name)
        self.style().polish(self.name)
        super().update()


    def __change_icon(self):
        pm = self.get_pixmap(self.__icon_name, self.__icon_size)
        self.set_icon(pm)


    def _refresh(self):
        self.__change_icon()



