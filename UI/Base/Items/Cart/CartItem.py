from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from UI.Base.Items.BaseItem import FilterItem


# Header Item Class for queue and status filter



class CartItem(FilterItem):
    
    def __init__(self, icon, name):
        super().__init__()

        self._name(name)

        pm = self.get_pixmap(self.path_name + icon)
        self.set_icon(pm)
        

        txt = 'cart'
        self.setObjectName(txt)

        self.__apply_style()


    def _name(self, name):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 0, 0, 0)
        self.mainLayout.addLayout(layout)
        
        txt = 'name'
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


    def __apply_style(self):
        style = '''

        #cart {
            border-top : 3px solid transparent;
        }

        #cart:hover {
            background-color : #ddf;
        }

        #cart[css-class="selected"] {
            border-top-color : blue;

            /* background-color : qlineargradient(x1 : 0.5, y1 : 0, x2 : 0.5, y2 : 1,
                                stop : 0 #ddf,
                                stop : 0.35 #ddf,
                                stop : 1 #fff);
            */
        }

        #name {
            color : darkcyan;
            font-family : Arial;
            font-size : 14px;
            font-weight : 600;
            padding : 0px 20px 0px 0px;
        }
        '''

        self.setStyleSheet(style)
















