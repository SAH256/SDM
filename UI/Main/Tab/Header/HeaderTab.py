from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt



class HeaderTab(QtWidgets.QScrollArea):
    
    def __init__(self, parent):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        name = 'tab-widget'

        self.wid = QtWidgets.QWidget()
        self.wid.setObjectName(name)
        self.wid.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.wid.setLayout(self.mainLayout)

        self.setWidget(self.wid)
        self.setWidgetResizable(True)

        h = 45
        self.setFixedHeight(h)

        self.selected = None

        self.items = []

        self._scroll()
        self._cart()

        name = 'header-tab'
        self.setObjectName(name)


    def _cart(self):
        self.cartLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.cartLayout)


    def _scroll(self):
        sc = QtWidgets.QScrollBar(Qt.Orientation.Horizontal)
        self.setHorizontalScrollBar(sc)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)




