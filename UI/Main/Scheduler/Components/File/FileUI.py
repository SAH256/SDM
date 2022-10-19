
from PyQt5 import QtWidgets

from UI.Base.Button.StyledButton import StyleButton
from Utility.Core import ICONS

from .Tree import View


# File view for managing tasks in a queue -- UI class
class FileUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self._table()
        self._buttons()


    def _table(self):
        tableLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(tableLayout)

        self.table = View()

        tableLayout.addWidget(self.table)


    def _buttons(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 5, 0, 10)
        self.mainLayout.addLayout(layout)

        buttons = [
            ('upBtn', ICONS.OTHER.MOVE_UP),
            ('downBtn', ICONS.OTHER.MOVE_DOWN),
            ('delBtn', ICONS.OTHER.TRASH),
            None
        ]

        for item in buttons:

            if item:
                wid = StyleButton(item[1], '')
                wid.icon_selector(True)

                layout.addWidget(wid)
                setattr(self, item[0], wid)
            else:
                layout.addStretch()

