from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from Utility.Gui import get_icon
from Utility.Core import SELECTORS

# Base class of all GUI Items that is using.


class BaseItem(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent = parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.mainLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.LeftToRight)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.mainLayout)

        self.cache = QtGui.QPixmapCache()

        self._icon()

        self.path_name = 'Icons'
        self.selected = False
        self.entered = False


    def _icon(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 5, 10, 5)
        self.mainLayout.addLayout(layout)

        # name = 'lkm.lskjdlkjl'
        # icon = iconFinder(name)

        self.iconPlace = QtWidgets.QLabel(self)
        # self.iconPlace.setPixmap(icon.pixmap(32, 32))
        layout.addWidget(self.iconPlace)



    def set_icon(self, pixmap):
        self.iconPlace.setPixmap(pixmap)


    def get_pixmap(self, key, size = 32):
        pixmap = self.cache.find(key)

        if not pixmap:
            icon = get_icon(key)
            if not icon.isNull():
                pixmap = icon.pixmap(size, size)
                self.cache.insert(key, pixmap)

        return pixmap

    def set_selected(self, s):
        self.selected = s

    def set_hover(self, s):
        self.hover = s
    
    def _refresh(self):
        pass

    def is_selected(self):
        return self.selected

    def update(self):
        self.style().unpolish(self)
        self.style().polish(self)
        super().update()

    def enterEvent(self, ev):
        super().enterEvent(ev)
        self.entered = True

    def leaveEvent(self, ev):
        super().leaveEvent(ev)
        self.entered = False

# Filter class for category and status items
class FilterItem(BaseItem):

    def __init__(self, parent):
        super().__init__(parent)

        self._type = None
        self.data = None

        layout = self.mainLayout.itemAt(0)
        layout.setContentsMargins(0, 0, 0, 0)


    def set_selected(self, s):
        super().set_selected(s)

        value = ''
        if s:
            value = SELECTORS.VALUE.SELECTED
        
        self.setProperty(SELECTORS.PROPERTY.CSS_CLASS, value)
        self.update()
    
    def set_type(self, _type):
        self._type = _type

    def set_data(self, data):
        self.data = data

