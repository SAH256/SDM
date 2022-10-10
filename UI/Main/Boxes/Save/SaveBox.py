
from PyQt5 import QtWidgets, QtGui

from UI.Base.Input.StyledInput import StyleInput
from UI.Base.Button.StyledButton import StyleButton

from Utility.Core import ICONS


# Save path selector widget -- UI class
class SavePath(QtWidgets.QWidget):

    OK = 'ok-state'
    DANGER = 'danger-state'
    
    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.mainLayout.setContentsMargins(0, 5, 0, 5)
        self.mainLayout.setSpacing(10)

        self._widgets = []

        self._info()
        self._path()
        
        name = 'save-box'
        self.setObjectName(name)


    def _info(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)

        txt = 'N/A'

        data = [
            (None, 'Storage:'),
            ('free_space', txt),
            (None, '/'),
            ('total_space', txt),
            (None, ','),
            ('percentage', txt),
            (None, 'free'),
            None
        ]


        for item in data:
            if item:
                wid = QtWidgets.QLabel(item[1])
                layout.addWidget(wid)

                if item[0]:
                    self._widgets.append(wid)
                    setattr(self, item[0], wid)
            else:
                layout.addStretch()


    def _path(self):
        self.pathLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.LeftToRight)
        self.mainLayout.addLayout(self.pathLayout)

        self.__history()
        self.__path_box()
        self.__btn()


    def __history(self):
        historyLayout = QtWidgets.QHBoxLayout()
        self.pathLayout.addLayout(historyLayout)

        ico = ICONS.OTHER.FOLDER_1
        s = 20

        self.history = QtWidgets.QLabel()
        self.history.setPixmap(QtGui.QIcon(ico).pixmap(s, s))

        historyLayout.addWidget(self.history)


    def __path_box(self):
        boxLayout = QtWidgets.QHBoxLayout()
        self.pathLayout.addLayout(boxLayout, 12)

        self.save_box = StyleInput()

        boxLayout.addWidget(self.save_box)


    def __btn(self):
        btnLayout = QtWidgets.QHBoxLayout()
        self.pathLayout.addLayout(btnLayout)

        self.browseBtn = StyleButton(ICONS.OTHER.BROWSE_1, '')

        btnLayout.addWidget(self.browseBtn)
    
    def update(self, wid):
        self.style().unpolish(wid)
        self.style().polish(wid)
        super().update()

