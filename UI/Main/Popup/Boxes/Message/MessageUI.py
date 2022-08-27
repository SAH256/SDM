
from PyQt5 import QtWidgets

from UI.Base.Dialog.Frameless.Base import FrameLessUI
from UI.Base.Button.StyledButton import StyleButton

from Utility.Core import SELECTORS


class Message(FrameLessUI):

    def __init__(self, parent):
        super().__init__(parent)

        self._label()
        self.mainLayout.addStretch(1)
        self._buttons()

        self.__style()
    

    def _label(self):
        layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(layout)

        self.info_label = QtWidgets.QLabel()

        layout.addWidget(self.info_label)



    def _buttons(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)

        text = 'OK'
        self.okBtn = StyleButton(None, text)
        self.okBtn.set_type(SELECTORS.STATES.CONFIRM)

        layout.addWidget(self.okBtn)
    

    def set_data(self, text):
        self.__setup(text)


    def __setup(self, text):
        self.okBtn.clicked.connect(self.close)

        self.info_label.setText(text)
    

    def __style(self):
        style = '''
        #info {
            font-family : Arial;
            font-size : 14px;
            font-weight : 600;
            color : #444;
        }
        '''

        self.info_label.setStyleSheet(style)















