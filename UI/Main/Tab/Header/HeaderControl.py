from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from UI.Base.Items.Cart.CartItem import CartItem

from Utility.Core import FILTER

from .HeaderTab import HeaderTab


class HeaderControl(HeaderTab):

    item_changed = QtCore.pyqtSignal(list)

    def add_item(self, icon, name, _type, data):
        item = self.__get_item(icon, name, _type, data)
        self.items.append(item)


    def remove_item(self, name):
        
        index = self.exist(name)

        if index >= 0:
            item = self.items[index]

            self.mainLayout.removeWidget(item)
            self.items.remove(item)

            if self.selected == item:
                prev = self.items[index - 1]
                self.__change_selection(prev)


    def exist(self, name):
        result = -1

        for index, item in enumerate(self.items):
            if item.get_name() == name:
                result = index
                break

        return result


    def __get_item(self, icon, name, _type, data):
        item = CartItem(icon, name)
        item.set_type(_type)
        item.set_data(data)

        if not self.selected:
            item.set_select(True)
            self.selected = item

        self.mainLayout.addWidget(item)

        return item


    def mouseReleaseEvent(self, ev):
        super().mouseReleaseEvent(ev)

        self.setFocus()
        if ev.button() == Qt.MouseButton.LeftButton:

            child = self.childAt(ev.pos())

            if child and not isinstance(child, CartItem):
                child = child.parentWidget()

            if child and isinstance(child, CartItem):
                if child != self.selected:
                    self.__change_selection(child)
                    self.ensureWidgetVisible(child)


    def __change_selection(self, item):

        if self.selected:
            self.selected.set_select(False)

        item.set_select(True)
        self.selected = item

        self.item_changed.emit([item._type, item.data])


    def wheelEvent(self, ev):
        super().wheelEvent(ev)

        d = ev.angleDelta().y() * -1

        sc = self.horizontalScrollBar()
        sc.setValue(sc.value() + d // 15)


    def enterEvent(self, ev):
        super().enterEvent(ev)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)


    def leaveEvent(self, ev):
        super().enterEvent(ev)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


    def check_queues(self, existing):
        items = [item for item in self.items if item._type == FILTER.QUEUE]

        for item in items:
            if item.get_name() not in existing:
                self.remove_item(item.get_name())


