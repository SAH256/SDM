from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from UI.Base.Menu.StyledMenu import StyleMenu

from UI.Base.Items.Task.TaskItemControl import TaskItemControl
from UI.Base.ScrollBar.ScrollBarUI import StyleScrollBar

from .Models import FilterModel
from .Util import ItemDel, MItem


# Task list view in main ui
class View(QtWidgets.QListView):

    selection_changed = QtCore.pyqtSignal(list)
    menu_requested = QtCore.pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.__model = QtGui.QStandardItemModel()
            
        self.proxy = FilterModel(self.__model)

        self.setModel(self.proxy)

        self.setEditTriggers(self.EditTrigger.NoEditTriggers)

        widget = TaskItemControl()
        d = ItemDel(widget)
        self.setItemDelegate(d)

        self.items = {}

        name = 'view'
        self.setObjectName(name)

        self.setSelectionMode(self.SelectionMode.ExtendedSelection)

        self.selectionModel().selectionChanged.connect(self.__selection_handler)

        self.__scroll()
        self.__timer()

        self.__apply_style()


    def add_task(self, info):

        if self.items.get(info):
            return

        item = MItem(info)
        self.items[info] = item
        self.__model.appendRow(item)


    def __scroll(self):
        sc = StyleScrollBar(Qt.Orientation.Vertical)
        self.setVerticalScrollBar(sc)


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


    def __apply_style(self):
        style = '''

        #view {
            outline : none;
            border : none;
            background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5,
              stop: 0 white,
              stop: 0.5 #ddd,
              stop: 1 white);
        }

        #view::item {
            margin : 3px 5px;
            padding : 25px 10px;
            background-color : white;
            border-radius : 3px;
        }

        #view::item:hover {
            background-color : #c2d7fc;
        }

        #view::item:selected {
            background-color : #cbebff;
            border : 2px solid blue;
        }
        '''

        self.setStyleSheet(style)

