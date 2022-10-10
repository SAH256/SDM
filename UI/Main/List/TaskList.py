from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from UI.Base.Items.Task.TaskItemControl import TaskItemControl

from .Models import FilterModel
from .Util import ItemDel, MItem


# Task list view in main ui
class View(QtWidgets.QListView):

    selection_changed = QtCore.pyqtSignal(list)
    menu_requested = QtCore.pyqtSignal(list)

    def __init__(self, parent):
        super().__init__(parent)

        self.__model = QtGui.QStandardItemModel()
        self.proxy = FilterModel(self.__model)
            

        self.setModel(self.proxy)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setSelectionMode(self.SelectionMode.ExtendedSelection)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)
        self.selectionModel().selectionChanged.connect(self.__selection_handler)

        widget = TaskItemControl(self)
        widget.setVisible(False)
        d = ItemDel(widget)
        self.setItemDelegate(d)

        self.items = {}

        name = 'task-list'
        self.setObjectName(name)

        self.__timer()


    def add_task(self, info):
    
        if self.items.get(info):
            return

        item = MItem(info)
        self.items[info] = item
        self.__model.appendRow(item)
        


    def __timer(self):
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.__update)

        self.timer.start(500)


    def __update(self):
        first = self.indexAt(self.rect().topLeft())
        last = self.indexAt(self.rect().bottomLeft())

        self.dataChanged(first, last)
        self.__selection_handler()


    def __selection_handler(self):
        indices = self.selectedIndexes()
        selected = []

        for index in indices:
            info = index.data(MItem.PRIVATE_ROLE)

            if info:
                selected.append(info.state)

        self.selection_changed.emit(selected)


    def get_selected(self):
        indices = self.selectedIndexes()

        selected = []

        for index in indices:
            info = index.data(MItem.PRIVATE_ROLE)

            if info:
                selected.append(info._id)

        return selected


    def remove_task(self, _id):
        data = filter(lambda data : data[0]._id == _id, self.items.items())
        data = list(data)

        # just for cleaning indexing and in case of more than one element
        for info, item in data:
            self.items.pop(info)
            self.__remove_item(item)


    def __remove_item(self, item):
        item.clearData()
        self.__model.removeRow(item.row())


    def filter_data(self):
        self.proxy.invalidate()
        self.proxy.invalidateFilter()


    def set_name(self, name):
        self.proxy.set_name(name)

    def set_queue(self, queue):
        self.proxy.set_queue(queue)

    def set_category(self, cat):
        self.proxy.set_category(cat)

    def set_status(self, status):
        self.proxy.set_status(status)

    def set_state(self, state):
        self.proxy.set_state(state)


    def contextMenuEvent(self, ev):
        super().contextMenuEvent(ev)

        if len(self.selectedIndexes()) > 1:
            return

        index = self.indexAt(ev.pos())
        
        if index != self.__model.invisibleRootItem().index():
            info = index.data(MItem.PRIVATE_ROLE)
            pos = ev.globalPos()

            self.menu_requested.emit([info, pos])


    def enterEvent(self, ev):
        super().enterEvent(ev)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)


    def leaveEvent(self, ev):
        super().leaveEvent(ev)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


