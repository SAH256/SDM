
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class StyleScrollBar(QtWidgets.QScrollBar):

    def __init__(self, orientation):
        super().__init__(orientation)

        margins = (5, 4, 5, 4)
        
        if orientation == Qt.Orientation.Vertical:
            margins = margins[::-1]

        self.setContentsMargins(*margins)




