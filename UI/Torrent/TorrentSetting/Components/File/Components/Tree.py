import time

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from UI.Base.ScrollBar.ScrollBarUI import StyleScrollBar

from Utility.Structure.Task.Base import File
from Utility.Core import PRIORITY
from Utility.Util import sizeChanger
from Utility.Gui import iconFinder


from .Delegate import Combo
from .Item import MItem



# File tree view widget for displaying file and folders releation
class View(QtWidgets.QTreeView):

    NAME = 0
    STATUS = 1
    SIZE = 2
    PRIORITY = 3

    setting_changed = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        header = ['Name', 'Status', 'Size', 'Priority', '']

        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(header)
        self.__model = model

        self.setModel(model)
        self.header().setDefaultSectionSize(120)
        self.header().setSectionsMovable(False)


        self.combo_d = Combo()
        self.setItemDelegateForColumn(3, self.combo_d)


        ind = 15
        self.setIndentation(ind)

        self.setEditTriggers(self.EditTrigger.AllEditTriggers)

        self.parents = []
        self.objects = []
        
        self.__scroll_bar()
        self.__manage_size()
        
        name = 'file-tree'
        self.setObjectName(name)
    
        self.__connect_slots()
    


    def __connect_slots(self):
        self.expanded.connect(self.__expand_handler)
        self.__model.itemChanged.connect(self.__change_handler)
        self.__model.itemChanged.connect(self.__signal_handler)


    def __scroll_bar(self):
        sc = StyleScrollBar(Qt.Orientation.Vertical)
        self.setVerticalScrollBar(sc)

        sc = StyleScrollBar(Qt.Orientation.Horizontal)
        self.setHorizontalScrollBar(sc)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        

    def enterEvent(self, ev):
        super().enterEvent(ev)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)


    def leaveEvent(self, ev):
        super().enterEvent(ev)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


    def __manage_size(self):
        self.setColumnWidth(0, 250)

        for i in range(1, self.__model.columnCount() - 1):
            self.setColumnWidth(i, 70)


    # creating row list of items for each column
    def create_row(self, parent = None, file = False):

        f = MItem('', checkable = True, file = file)

        temp = [f]

        for _ in range(self.__model.columnCount() - 1):
            temp.append(MItem())
        
        if file:
            
            temp[self.PRIORITY].setEditable(True)
        else:
            f.appendRow(QtGui.QStandardItem())


        if not parent:
            parent = self.__model.invisibleRootItem()

        return temp


    # populate row list items from file or folder object
    def _setup_row(self, row, item, file = False):

        row[self.NAME].set_prop(iconFinder(item.get_name(), is_folder = not file), item.get_name())
        row[self.NAME].setData(item, MItem.DATA_ROLE)

        c = None

        if file:
            row[self.SIZE].setText(sizeChanger(item.get_size()))

            s = 'Normal'
            p = item.get_priority()

            c = Qt.CheckState.Unchecked
                
            if p:
                c = Qt.CheckState.Checked
                s = PRIORITY.PRIORITIES_INDEX.get(p)

            row[self.PRIORITY].setData(s, Qt.ItemDataRole.EditRole)


        else :
            c = Qt.CheckState.PartiallyChecked
            state = item.is_selected()
            
            if state == True:
                c = Qt.CheckState.Checked
            elif state == False:
                c = Qt.CheckState.Unchecked
        

        if c == Qt.CheckState.Unchecked:
            self.enable_item(row, False)
        
        row[self.NAME].setCheckState(c)
            

    # add row list items to tree
    def add_row(self, parent, row):
        if not parent:
            parent = self.__model.invisibleRootItem()
        
        parent.appendRow(row)



    # enable / disable row items and controls
    def enable_item(self, items, state):
        temp = items

        if not isinstance(items, list):
            temp = []

            for c in range(1, self.__model.columnCount()):
                i = self.__model.sibling(items.row(), c, items.index())
                it = self.__model.itemFromIndex(i)
                temp.append(it)
        else:
            temp = temp[1:]    

        
        for it in temp:
            it.setEnabled(state)

            
    def __signal_handler(self):
        self.setting_changed.emit(True)


    # item data change handler in case of check and uncheck
    def __change_handler(self, item):

        file =  item.data(Qt.ItemDataRole.UserRole + 1)

        state = item.checkState()

        d = False
        if state == Qt.CheckState.Checked:
            d = True

        if file:
            self.enable_item(item, d)
        else:

            if state != Qt.CheckState.PartiallyChecked:
                if item.hasChildren():
                    self.parents.append(item)
                    self.__manage_children(item)
                    self.parents.remove(item)
   

        if item.isCheckable():
            p = item.parent()

            if p and p not in self.parents:
                self.parents.append(p)
                self.__manage_parent(p)
                self.parents.remove(p)


    # change check state of children base on parent check state
    def __manage_children(self, item):

        state = item.checkState()

        for i in range(item.rowCount()):
            child = item.child(i, 0)
            child.setCheckState(state)


    # change check state of parent base on its children
    def __manage_parent(self, item):
        state = None

        pat = [False, None, True]
        data = [pat[item.child(r, 0).checkState()] for r in range(item.rowCount())]


        if all(data):
            state = Qt.CheckState.Checked
        elif data.count(False) == len(data):
            state = Qt.CheckState.Unchecked
        else:
            state = Qt.CheckState.PartiallyChecked
        
        if item.checkState() != state:
            item.setCheckState(state)


    def get_item(self, index):
        return self.__model.itemFromIndex(index)


    # remove row and its children
    def _remove(self, parent = None):
        
        if not parent:
            parent = self.__model.invisibleRootItem()
            self._reset()
        
        for r in range(parent.rowCount()):
            
            item = parent.child(r, 0)
            
            if item.hasChildren():
                self._remove(item)
            
            item.clearData()                                            # remove python-obj data
            last = parent.child(r, parent.columnCount() - 1)
            if last:
                last.clearData()       # remove type data
            
        parent.removeRows(0, parent.rowCount())
        


    def __get_first_child(self):
        item = None

        p = self.__model.invisibleRootItem()

        if p.hasChildren():
            item = p.child(0, 0)

        return item



    def _select_all(self, state):

        item = self.__get_first_child()

        if item:
            item.setCheckState(state)
        

    # apply file or folder state from GUI to MODEL
    def _apply(self, parent = None):
        
        if not parent:
            parent = self.__model.invisibleRootItem()
        
        for r in range(parent.rowCount()):
            item = parent.child(r, self.NAME)
            first_child  = item.child(0, self.NAME)

            prio = parent.child(r, self.PRIORITY)
            
            
            if item.hasChildren() and first_child.isCheckable():
                self._apply(item)
            
            else:

                if item.isCheckable():
                    is_file = item.data(Qt.ItemDataRole.UserRole + 1)
                    obj = item.get_object()
                    priority = 0
                    
                    if item.checkState() == Qt.CheckState.Checked:
                        priority = PRIORITY.PRIORITIES.get(PRIORITY.NORMAL)

                        if is_file:

                            text = prio.data(Qt.ItemDataRole.EditRole)
                            prio_value = PRIORITY.PRIORITIES.get(text) 
                            if prio_value:
                                priority = prio_value

                    obj.set_priority(priority)


    # reset GUI to MODEL data
    def _reset(self):

        self.blockSignals(True)
        self.__reset_state()
        self.blockSignals(False)


    def __reset_state(self, parent = None):
        if not parent:
            parent = self.__model.invisibleRootItem()
        
        for r in range(parent.rowCount()):
            item = parent.child(r, self.NAME)
            
            
            if item.hasChildren():
                self.__reset_state(item)
            
            else:

                if item.isCheckable():
                    obj = item.get_object()

                    if obj:
                        p = obj.get_priority()
                        s = Qt.CheckState.Unchecked

                        if p:
                            s = Qt.CheckState.Checked
                            p = PRIORITY.PRIORITIES_INDEX.get(p)

                            if p:
                                sib = self.__get_sibling(r, self.PRIORITY, item.index())
                                
                                sib.setData(p, Qt.ItemDataRole.EditRole)
                        
                        item.setCheckState(s)

                else:
                    p = item.parent()
                    obj = p.get_object()

                    s = Qt.CheckState.PartiallyChecked
                    c = obj.is_selected()

                    if c == True:
                        s = Qt.CheckState.Checked
                    elif c == False:
                        s = Qt.CheckState.Unchecked
                    
                    p.setCheckState(s)


    def __get_sibling(self, row, col, base):
        index = self.__model.sibling(row, col, base)

        if index:
            return self.__model.itemFromIndex(index)
                                
    # update files status in tree
    def _update(self, parent = None):

        if not parent:
            parent = self.__model.invisibleRootItem()
        

        for r in range(parent.rowCount()):

            item = parent.child(r, self.NAME)

            if item.hasChildren():
                if self.isExpanded(item.index()):
                    self._update(item)
            else:
                obj = item.get_object()
                p = obj.get_progress()

                sib = self.__get_sibling(r, self.STATUS, item.index())
                
                if p > 0 and sib.text() != '100 %':
                    sib.setText(f'{round(p, 4)} %')
                elif sib.text():
                    sib.setText('')



    def hasItems(self):
        return self.__model.invisibleRootItem().hasChildren()


    # expand all the folder rows to display all their items
    def __expand_handler(self, index):
        
        item = self.get_item(index)
        obj = item.data(item.DATA_ROLE)

        child = ''

        if item.hasChildren():
            child = item.child(0, 0).text()
            
        if not child:
            item.removeRow(0)

            for folder in obj.get_folders():
                self._add_item(item, folder)
                
                
            for file in obj.get_files():
                self._add_item(item, file)


    # add file or folder model object to display in tree
    def _add_item(self, parent, item):
        is_file = type(item) == File

        row = self.create_row(parent, is_file)
        self._setup_row(row, item, is_file)
        self.add_row(parent, row)



    def __collapse_handler(self, index):
        item = self.__model.itemFromIndex(index)
        child = item.child(0, 0)

        _max = 50

        if child.isCheckable():
            r = item.rowCount()
            
            if r <= _max:
                self._remove(item)
                item.appendRow(QtGui.QStandardItem())
                


