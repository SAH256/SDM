from PyQt5 import QtCore

from Utility.Core import CATEGORY

from .CategoryUI import CategoryUI


# Category selector mini widget -- UI class
class CategoryControl(CategoryUI):

    category_changed = QtCore.pyqtSignal(str)

    def __init__(self, items):
        super().__init__()

        self.category.addItems(items)

        self.__connect_slots()

    def __connect_slots(self):
        self.category.currentIndexChanged[str].connect(self.__item_handler)


    def set_category(self, cat):
        self.category.setCurrentText(cat)


    def get_category(self):
        return self.category.currentText()


    def __item_handler(self, cat):
        self.category_changed.emit(cat)


    def _reset(self):
        self.category.setCurrentText(CATEGORY.GENERAL)


