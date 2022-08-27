from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from UI.Base.Items.Option.OptionItem import OptionItem



class OptionTab(QtWidgets.QWidget):

    item_changed = QtCore.pyqtSignal(list)
    
    def __init__(self, direction):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.mainLayout = QtWidgets.QBoxLayout(direction)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)

        self.items = []

        self.selected = None


    def add_item(self, icon, name, _type, data):
        item = self.__get_item(icon)
        item.set_type(_type)
        item.set_data(data)

        item.setToolTip(name)
        self.items.append(item)


    def __get_item(self, icon):
        item = OptionItem(icon)

        if not self.selected:
            item.set_select(True)
            self.selected = item

        self.mainLayout.addWidget(item)

        return item


    def add_space(self, d):
        if d > 0:
            self.mainLayout.addStretch(d)


    def mouseReleaseEvent(self, ev):
        super().mouseReleaseEvent(ev)

        self.setFocus()
        if ev.button() == Qt.MouseButton.LeftButton:

            child = self.childAt(ev.pos())

            if child and not isinstance(child, OptionItem):
                child = child.parentWidget()

            if child and isinstance(child, OptionItem):
                if child != self.selected:
                    self.__change_selection(child)


    def __change_selection(self, item):

        if self.selected:
            self.selected.set_select(False)

        item.set_select(True)
        self.selected = item

        self.item_changed.emit([item._type, item.data])


