from PyQt5 import QtGui
from PyQt5.QtCore import Qt



# Customized item for populating file tree
class MItem(QtGui.QStandardItem):

    TYPE_ROLE = Qt.ItemDataRole.UserRole + 1
    DATA_ROLE = Qt.ItemDataRole.UserRole + 2

    def __init__(self, text = None, icon = None, checkable = False, file = None):
        super().__init__()
        
        f = self.font().family()
        font = QtGui.QFont(f, 8)

        if checkable:
            font.setFamily('Arial')
            font.setPointSize(10)

            self.setCheckable(True)
            
            if not file:
                self.setAutoTristate(True)
        
            self.setData(file)

            self.setCheckState(Qt.CheckState.Unchecked)

        self.setDragEnabled(False)
        self.setDropEnabled(False)
        self.setEditable(False)

        self.setFont(font)

        self.set_prop(icon, text)

    
    def setData(self, value, role = TYPE_ROLE):
        return super().setData(value, role)
        

    def set_prop(self, icon = None, text = None):

        if icon:
            self.setIcon(icon)

        if text:
            self.setText(text)

    def get_object(self):
        item = self

        if self.index().column():
            item = self.model().sibling(self.index().row(), 0, self.index())
        
        return item.data(self.DATA_ROLE)


    def is_file(self):
        item = self

        if self.index().column():
            item = self.model().sibling(self.index().row(), 0, self.index())

        return item.data(self.TYPE_ROLE)

