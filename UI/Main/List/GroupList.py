
from PyQt5.QtWidgets import QTreeView, QScrollBar
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSignal

from Utility.Util import sizeChanger, split_file_name
from Utility.Gui import iconFinder, findCategory
from Utility.Core import HTTP

from .Util import MItem


# Group dialog files list view
class View(QTreeView):
    NAME = 0
    STATUS = 1
    SIZE = 2
    CATEGORY = 3
    PENDING = 'Pending...'
    OK = 'OK'

    selection_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        header = ['Name', 'Status', 'Size', 'Category']

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(header)
        self.__model = model

        self.setModel(model)
        self.header().setDefaultSectionSize(120)
        self.header().setSectionsMovable(False)
        self.header().resizeSection(0, 400)


        self.setIndentation(0)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)
        self.setSelectionMode(self.SelectionMode.MultiSelection)
        self.selectionModel().selectionChanged.connect(self.__send_info)

        self.items = {}

        name = 'group-list'
        self.setObjectName(name)

        self.__scroll()


    def __scroll(self):
        sc = QScrollBar(Qt.Orientation.Vertical)
        self.setVerticalScrollBar(sc)


    def add_item(self, _id):
        na = 'n/a'
        row = self.__create_row()

        row[self.NAME].setIcon(iconFinder(na))
        row[self.STATUS].setText(self.PENDING)
        row[self.SIZE].setText(na)
        row[self.CATEGORY].setText(na)

        self.__model.appendRow(row)
        self.items[_id] = row[self.NAME]


    def __create_row(self):
        row = [MItem()]
        row.extend([QStandardItem() for x in range(3)])

        return row


    def set_pattern(self, pattern):
        for _id, item in self.items.items():
            name = pattern.format(str(_id))
            item.setText(name)


    def set_data(self, _id, data):
        item = self.items.get(_id)

        if item:
            item.setData(data, MItem.PRIVATE_ROLE)
            select = self.__setup_item(item, data)

            if select:
                self.selectionModel().select(item.index(), self.selectionModel().SelectionFlag.Rows | self.selectionModel().SelectionFlag.Select)


    def __setup_item(self, item, data):
        status = ''
        size = 'n/a'
        cat = 'n/a'
        select = False

        if data.is_successful():
            status = self.OK
            size = sizeChanger(data.size)
            cat = findCategory(split_file_name(data.name)[-1])
            item.setIcon(iconFinder(data.name))
            select = True
        else:
            status = HTTP.RESPONSE.ERROR_STATUS.get(data.code)
            status = str(status)

        self.__model.item(item.row(), self.STATUS).setText(status)
        self.__model.item(item.row(), self.SIZE).setText(size)
        self.__model.item(item.row(), self.CATEGORY).setText(cat)


        return select


    # send size and count of selected to dialog
    def __send_info(self):
        size = 0
        count = 0
        selected = self.selectedIndexes()

        for item in self.items.values():

            if item.index() not in selected:
                continue

            data = item.data(MItem.PRIVATE_ROLE)

            if data:
                size += data.size

            count += 1

        self.selection_changed.emit([size, count])
    

    def select_all(self, state):
    
        if state:
            self.selectAll()
        else:
            self.selectionModel().clearSelection()


    # get metadata of items
    def get_data(self):
        selected = self.selectedIndexes()
        items_data = {}

        for _id, item in self.items.items():
            if item.index() in selected:
                data = item.data(MItem.PRIVATE_ROLE)
                items_data[_id] = data

        return items_data



