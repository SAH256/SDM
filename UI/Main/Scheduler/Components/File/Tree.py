
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from Utility.Core import LINK_TYPE, STATES
from Utility.Gui import iconFinder
from Utility.Calcs import format_remain_time
from Utility.Util import sizeChanger



class Item(QtGui.QStandardItem):

    PRIVATE_ROLE = Qt.ItemDataRole.UserRole + 1

    def __init__(self):
        super().__init__()

        f = QtGui.QFont(self.font().family(), 9)
        self.setFont(f)

    def set_data(self, info):
        self.setData(info, self.PRIVATE_ROLE)



# File tree view of Scheduler dialog
class View(QtWidgets.QTreeView):

    NAME = 0
    STATUS = 1
    SIZE = 2
    TIME = 3

    def __init__(self):
        super().__init__()

        headers = ['File Name', 'Status', 'Size', 'Time Left']

        self.__model = QtGui.QStandardItemModel()
        self.__model.setHorizontalHeaderLabels(headers)
        self.setModel(self.__model)

        self.header().setSectionsMovable(False)
        self.header().setDefaultSectionSize(120)

        self.setIndentation(0)
        self.setDragEnabled(True)

        self.setSelectionMode(self.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)

        name = 'table'
        self.setObjectName(name)

        self.__apply_style()


    def create_row(self, info):
        
        row = [Item() for _ in range(self.__model.columnCount())]

        row[self.NAME].setIcon(QtGui.QIcon(iconFinder(info.name, info._type == LINK_TYPE.MAGNET)))
        row[self.NAME].setText(info.name)
        row[self.SIZE].setText(sizeChanger(info.total_size))

        row[self.NAME].set_data(info)

        parent = self.__model.invisibleRootItem()
        parent.appendRow(row)


    def _reset(self):

        for r in range(self.__model.rowCount()):
            self.__model.item(r, 0).clearData()

        self.__model.removeRows(0, self.__model.rowCount())


    def remove_selected(self):
        indices = self.selectionModel().selectedRows(0)
        items = [self.__model.itemFromIndex(x) for x in indices]

        result = []

        for item in items:
            data = item.data(Item.PRIVATE_ROLE)
            result.append(data._id)
            item.clearData()

            self.__model.removeRow(item.row())

        return result

    # move selected items base on user choice
    def move_selected(self, up = True):
        indices = self.selectionModel().selectedRows(0)
        indices.sort(key = lambda x : x.row(), reverse = not up)
        items = [self.__model.itemFromIndex(x) for x in indices]

        if items:

            for item in items:
                r = item.row()
                c = 0
                ind = None

                if up:
                    ind = self.indexAbove(item.index())
                else:
                    ind = self.indexBelow(item.index())

                p = self.__model.itemFromIndex(ind)

                if p not in items:

                    if up and r > 0:
                        c = -1
                    elif not up and r < self.__model.rowCount() - 1:
                        c = 1

                    if c:
                        row = self.__model.takeRow(r)
                        self.__model.insertRow(r + c, row)

                self.selectionModel().select(item.index(), self.selectionModel().SelectionFlag.Select | self.selectionModel().SelectionFlag.Rows)

            return self.__get_orders()


    def __get_orders(self):
        order = []

        for r in range(self.__model.rowCount()):
            item = self.__model.item(r, 0)
            data = item.data(Item.PRIVATE_ROLE)

            order.append(data._id)

        return order


    def startDrag(self, actions):

        indices = self.selectionModel().selectedRows(0)

        if indices:
            data = QtCore.QMimeData()
            temp = ''

            for ind in indices:
                info = ind.data(Item.PRIVATE_ROLE)
                if not temp:
                    temp = f'{info.queue}:'

                temp += f'{info._id}-'

            data.setText(temp)

            pixmap = self.__make_pixmap(indices)

            drag = QtGui.QDrag(self)
            drag.setPixmap(pixmap)
            drag.setMimeData(data)

            dda = Qt.DropAction.IgnoreAction

            if actions & Qt.DropAction.MoveAction and self.dragDropMode() != self.DragDropMode.InternalMove:
                dda = Qt.DropAction.MoveAction

            if drag.exec(actions, dda) == Qt.DropAction.MoveAction:
                items = [self.__model.itemFromIndex(ind) for ind in indices]

                for item in items:
                    self.__remove_row(item)


    def __remove_row(self, item):
        item.clearData()
        self.__model.removeRow(item.row())


    def __make_pixmap(self, indices):
        s = 32
        base = QtGui.QPixmap(s + len(indices) * (s//10), s)

        base.fill(Qt.GlobalColor.transparent)

        p = QtGui.QPainter(base)

        point = QtCore.QPoint(0, 0)

        for index in indices:
            icon = index.data(Qt.ItemDataRole.DecorationRole)
            p.drawPixmap(point, icon.pixmap(s, s))

            point.setX(point.x() + (s//10))

        return base


    def _update_info(self):

        for r in range(self.__model.rowCount() - 1, -1, -1):

            item = self.__model.item(r, self.NAME)
            info = item.data(Item.PRIVATE_ROLE)
            status = self.__model.item(r, self.STATUS)
            remain_time = self.__model.item(r, self.TIME)

            if info.state == STATES.RUNNING and info.downloaded > 0:
                status.setText(f'{round(info.downloaded * 100 / info.total_size, 2)} %')

                eta = 'N/A'

                if info.eta > -1:
                    eta = format_remain_time(info.eta)

                remain_time.setText(eta)

            if info.metadata and info.downloaded == info.total_size:
                self.__remove_row(item)


    def item_count(self):
        return self.__model.rowCount()


    def __apply_style(self):
        style = '''
        #table {
            outline : none;
            border : none;
        }

        #table::item {
            border-right : 1px solid #ddd;
            border-bottom : 1px solid #ddd;
            font-size : 12px;
        }

        #table::item:selected {
            background-color : #1452f4;
            border-right-color : white;
            color : white;
        }

        #table::item:hover:selected {
            color : white;
            border-radius : 2px;
        }

        QHeaderView::section {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #616161, stop: 0.5 #505050,
                                              stop: 0.6 #434343, stop:1 #656565);
            color: white;
            padding-left: 4px;
            border: 1px solid #6c6c6c;
            font-weight : 600;
        }
        '''

        self.setStyleSheet(style)

