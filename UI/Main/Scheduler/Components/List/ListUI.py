from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from UI.Base.Button.StyledButton import StyleButton
from Utility.Core import ICONS

from .View import List


# Queue list widget in Scheduler -- UI class
class ListUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.mainLayout)


        w1, w2 = 200, 220
        self.setMinimumWidth(w1)
        self.setMaximumWidth(w2)

        self._ribbon()
        self._list()

        self.mainLayout.addStretch(1)
        
        name = 'queue-list-container'
        self.setObjectName(name)



    def _ribbon(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(10, 10, 0, 5)
        self.mainLayout.addLayout(layout)

        txt = 'Queues'
        name = 'list-header'
        
        label = QtWidgets.QLabel(txt)
        label.setObjectName(name)
        label.setFixedHeight(30)

        layout.addWidget(label)

        buttons = [
            None,
            ('addBtn', ICONS.OTHER.ADD_1),
            ('removeBtn', ICONS.OTHER.TRASH)
        ]

        s = 25

        for item in buttons:
            if item:
                wid = StyleButton(item[1], '')
                wid.icon_selector(True)
                wid.setVisible(False)

                wid.setMaximumSize(s, s)

                layout.addWidget(wid)
                setattr(self, item[0], wid)

            else:
                layout.addStretch()


    def _list(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addLayout(layout)
        self.mainLayout.setStretchFactor(layout, 10)

        self.view = List()

        layout.addWidget(self.view)


    def enterEvent(self, ev):
        super().enterEvent(ev)

        self.__toggle_btn()


    def leaveEvent(self, ev):
        super().enterEvent(ev)

        self.__toggle_btn(False)

    def __toggle_btn(self, s = True):
        self.addBtn.setVisible(s)
        self.removeBtn.setVisible(s)





