
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from UI.Base.Dialog.Frameless.Base import FrameLessUI
from UI.Base.Button.StyledButton import StyleButton

from Utility.Core import SELECTORS


class Confirm(FrameLessUI):

    def __init__(self, parent):
        super().__init__(parent)

        w, h = 250, 150
        self.resize(w, h)

        self.is_confirmed = False

        self._label()
        self.mainLayout.addStretch(1)
        self._buttons()


    def __setup(self):
        self.cancelBtn.clicked.connect(self.close)
        self.confirmBtn.clicked.connect(self.__confirm_handler)


    def _label(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 10, 0, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addLayout(layout)

        text = 'Are You Sure?'
        name = 'popup-message'

        self.info_label = QtWidgets.QLabel(text)
        self.info_label.setObjectName(name)

        layout.addWidget(self.info_label)


    def _buttons(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)

        buttons = [
            ('cancelBtn', 'CANCEL', None),
            ('confirmBtn', 'CONFIRM', SELECTORS.STATES.CONFIRM)
        ]

        for item in buttons:
            wid = StyleButton(None, item[1])
            wid.set_type(item[2])
            

            layout.addWidget(wid)
            setattr(self, item[0], wid)


    def set_data(self, name):
        self.name = name

        self.__setup()


    def __confirm_handler(self):
        self.is_confirmed = True
        self.close()
    

    def exec(self):
        super().exec()

        return self.is_confirmed

