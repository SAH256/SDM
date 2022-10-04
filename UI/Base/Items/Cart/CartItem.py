from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from UI.Base.Items.BaseItem import FilterItem


# Header Item Class for queue and status filter



class CartItem(FilterItem):
    
    def __init__(self, parent, icon, name):
        super().__init__(parent)

        self._name(name)

        pm = self.get_pixmap(self.path_name + icon)
        self.set_icon(pm)
        

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

    def get_pixmap(self, key):
        super().get_pixmap()

        size = 18
        pixmap = self.cache.find(key)
        
        if not pixmap:

            icon = QtGui.QIcon(key)
            pixmap = icon.pixmap(size, size)
            self.cache.insert(key, pixmap)
        
        return pixmap


    def update(self):
        self.style().unpolish(self.name)
        self.style().polish(self.name)
        super().update()











