
from PyQt5 import QtGui
from PyQt5.QtWidgets import QListView, QScrollBar
from PyQt5.QtCore import Qt, pyqtSignal

from Utility.Core import ICONS



class Item(QtGui.QStandardItem):

    PRIVATE_ROLE = int(Qt.ItemDataRole.UserRole) + 1


    def __init__(self, txt, is_one_time = True):
        super().__init__(txt)

        self.setData(is_one_time, self.PRIVATE_ROLE)



# List view of queues in list widget ui 
class List(QListView):
    
    current_changed = pyqtSignal(str)
    item_dragged = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()

        self.__model = QtGui.QStandardItemModel()
        self.setModel(self.__model)

        self.setContentsMargins(0, 0, 0, 0)

        self.ONE_TIME = QtGui.QIcon(ICONS.OTHER.ONE_TIME)
        self.PERIODIC = QtGui.QIcon(ICONS.OTHER.PERIODIC)

        self.setEditTriggers(self.EditTrigger.NoEditTriggers)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

        name = 'queue-list'
        self.setObjectName(name)

        self.__connect_slots()
        self.__scroll()
    
    def __connect_slots(self):
        self.selectionModel().currentChanged.connect(self.__change_handler)


    def __scroll(self):
        sc = QScrollBar(Qt.Orientation.Vertical)
        self.setVerticalScrollBar(sc)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


    def __change_handler(self, s, d = None):

        if s:
            item = self.__model.itemFromIndex(s)

            self.current_changed.emit(item.text())


    def __create_row(self, name, is_one_time):
        item = Item(name, is_one_time)

        item.setIcon(self.ONE_TIME if is_one_time else self.PERIODIC)

        self.__model.invisibleRootItem().appendRow(item)

        if not self.selectionModel().hasSelection():
            self.selectionModel().select(item.index(), self.selectionModel().SelectionFlag.Select)
            self.__change_handler(item.index())


    def add_data(self, all_data):

        for data in all_data:
            items = self.__model.findItems(data[0])

            if not items:
                self.__create_row(*data)
            else:
                temp_item = items[0]

                if temp_item.data(Item.PRIVATE_ROLE) != data[1]:
                    temp_item.setData(data[1], Item.PRIVATE_ROLE)
                    temp_item.setIcon(self.ONE_TIME if data[1] else self.PERIODIC)


    def remove_item(self, name = None):

        row = None

        if not name:
            ind = self.currentIndex()
            name = self.__model.itemFromIndex(ind).text()
            row = ind.row()

        else:
            items = self.__model.findItems(name)

            if items:
                row = items[0].row()

        self.__model.removeRow(row)

        return name


    def selected_item(self):
        ind = self.currentIndex()
        item = self.__model.itemFromIndex(ind)

        return item.text()


    def dragEnterEvent(self, ev):
        if ev.mimeData().hasText():
            ev.acceptProposedAction()


    def dragMoveEvent(self, ev):
        index = self.indexAt(ev.pos())

        if index != self.__model.invisibleRootItem():
            item = self.__model.itemFromIndex(index)
            if item:
                ev.accept()
        else:
            ev.ingore()


    def dropEvent(self, ev):
        index = self.indexAt(ev.pos())
        dest = index.data(Qt.ItemDataRole.DisplayRole)

        if ev.mimeData().hasText() and dest:

            data = ev.mimeData().text()
            source, items = data.split(':')
            if source != dest:
                items = [x for x in items.split('-') if x]

                r = [source, dest, items]

                self.item_dragged.emit(r)

                ev.acceptProposedAction()

            else:
                ev.ignore()


    def enterEvent(self, ev):
        super().enterEvent(ev)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)


    def leaveEvent(self, ev):
        super().leaveEvent(ev)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)




