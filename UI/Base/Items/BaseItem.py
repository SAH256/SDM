from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from Utility.Gui import iconFinder


# Base class of all GUI Items that is using.


class BaseItem(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.mainLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.LeftToRight)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.mainLayout)

        self.cache = QtGui.QPixmapCache()

        self._icon()

        self.path_name = 'Icons'
        self.selected = False
        self.hovered = False

        self.select_value = 'selected'
        self.css_prop = 'css-class'


    def _icon(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 5, 10, 5)
        self.mainLayout.addLayout(layout)

        name = 'lkm.lskjdlkjl'
        icon = iconFinder(name)

        self.iconPlace = QtWidgets.QLabel()
        self.iconPlace.setPixmap(icon.pixmap(32, 32))
        layout.addWidget(self.iconPlace)



    def set_icon(self, pixmap):
        self.iconPlace.setPixmap(pixmap)


    def get_pixmap(self):
        pass


    def set_type(self, _type):
        self._type = _type

    def set_data(self, data):
        self.data = data

    def set_select(self, s):
        self.selected = s

    def set_hover(self, s):
        self.hover = s

    def _update(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


# Filter class for category and status items
class FilterItem(BaseItem):

    def __init__(self):
        super().__init__()

        self._type = None
        self.data = None

        layout = self.mainLayout.itemAt(0)
        layout.setContentsMargins(0, 0, 0, 0)


    def set_select(self, s):
        super().set_select(s)

        value = ''
        if s:
            value = self.select_value
        
        self.setProperty(self.css_prop, value)
        self._update()

