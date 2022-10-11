from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QTimer


from UI.Base.Delegate.ListDelegate import ListItemDelegate, MItem


class ListItemView(QtWidgets.QListView):
    
    def __init__(self, parent, item_wid, dynamic = False):
        super().__init__(parent)
        
        self.__model = QtGui.QStandardItemModel()
        self.setModel(self.__model)
        
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setSelectionMode(self.SelectionMode.NoSelection)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)
        
        d = ListItemDelegate(item_wid)
        self.setItemDelegate(d)

        self.items = {}
        self.paused = True
        self.dynamic = dynamic

        name = 'live-list'
        self.setObjectName(name)


        self.__timer()


    def update_data(self, info_data):
        
        if self.dynamic:
            self.__filter_items(info_data)

        for key, info in info_data.items():
            
            item = self.items.get(key)
            
            if not item:
                item = MItem(info)
                self.__add_item(key, item)

            item.setData(info)

    def __add_item(self, key, item):
        self.items[key] = item
        self.__model.appendRow(item)
    
    def __remove_item(self, key):
        item = self.items.pop(key)
        item.clearData()
        self.__model.removeRow(item.row())
        


    def __timer(self):
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.__update)

        self.timer.start(1000)


    def __update(self):
        
        if self.paused:
            return

        first = self.indexAt(self.rect().topLeft())
        last = self.indexAt(self.rect().bottomLeft())

        self.dataChanged(first, last)


    def __filter_items(self, new_data):
        parent = self.__model.invisibleRootItem()
        old_keys = list(self.items.keys())
        
        for key in old_keys:
            if key not in new_data:
                
                self.__remove_item(key)
                


    def set_paused(self, state):
        self.paused = state
        

    def _reset(self):
        parent = self.__model.invisibleRootItem()
        [item.clearData() for item in self.items.values()]
        self.items.clear()
        parent.removeRows(0, parent.rowCount())


