
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt

from UI.Base.Items.Tool.RoundItem import RoundItem
from UI.Base.Line.StyledLine import Line

from .OptionTab import OptionTab



class InfiniteControl(OptionTab):

    item_changed = QtCore.pyqtSignal(int)
    
    def __init__(self, parent, p_dir, line = True):
        super().__init__(parent, p_dir)
        
        s = 3
        if not line:
            s = 10

        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(s)
        
        self.need_line = line


        self.setAutoFillBackground(True)

        name = 'infinite-tab'
        self.setObjectName(name)
        




    def add_item(self, data, tip = ''):
        item = self.__get_item(data)
        item.setToolTip(tip)
        self.items.append(item)


    def __get_item(self, icon_name):
        item = RoundItem(self, icon_name)

        if len(self.items) and self.need_line:
            line = Line(False)
            self.mainLayout.addWidget(line, 0, Qt.AlignmentFlag.AlignCenter)

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

            if child and not isinstance(child, RoundItem):
                child = child.parentWidget()

            if child and isinstance(child, RoundItem):
                if child != self.selected:
                    self.__change_selection(child)


    def __change_selection(self, item):

        if self.selected:
            self.selected.set_select(False)

        item.set_select(True)
        self.selected = item

        self.item_changed.emit(self.items.index(item))




