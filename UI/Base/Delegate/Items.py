from PyQt5 import QtGui
from PyQt5.QtCore import Qt


# General view item that is using in group/task list
class MItem(QtGui.QStandardItem):

    PRIVATE_ROLE = int(Qt.ItemDataRole.UserRole) + 1

    def __init__(self, info = None):
        super().__init__()

        if info:
            self.setData(info)

    def set_data(self, data, role = PRIVATE_ROLE):
        super().set_data(data, role)




