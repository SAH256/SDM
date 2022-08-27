
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from UI.Base.Dialog.Frameless.Base import FrameLessUI
from UI.Base.ComboBox.StyledComboBox import ComboBox
from UI.Base.Button.StyledButton import StyleButton

from Utility.Core import DUPLICATE, SELECTORS


class Duplicate(FrameLessUI):

    def __init__(self, parent):
        super().__init__(parent)

        w, h = 300, 150
        self.resize(w, h)


        self.duplicate_option = False

        self._label()
        self._combo()
        self.mainLayout.addStretch(1)
        self._buttons()

        self.__style()

    
    def __setup(self):
        self.options.currentIndexChanged.connect(self.__option_handler)

        self.cancelBtn.clicked.connect(self.__cancel_handler)
        self.okBtn.clicked.connect(self.close)



    def _label(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 10, 0, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.mainLayout.addLayout(layout)

        text = 'What should we do?'
        name = 'info'

        self.info_label = QtWidgets.QLabel(text)
        self.info_label.setObjectName(name)

        layout.addWidget(self.info_label)
    

    def _combo(self):
        layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(layout)

        self.options = ComboBox()
        layout.addWidget(self.options)


        buttons = [
            (False, 'Do Nothing'),
            (DUPLICATE.NUMBER, 'Add duplicate with numbered file name'),
            (DUPLICATE.OVERWRITE, 'Add duplicate and overwite existing file'),
            (DUPLICATE.OPEN_RESUME, 'If completed open, otherwise resume it.'),
        ]

        for _id, txt in buttons:
            self.options.addItem(txt, _id)
    
        
        

    
    def _buttons(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)

        buttons = [
            ('cancelBtn', 'CANCEL', None),
            ('okBtn', 'OK', SELECTORS.STATES.CONFIRM),
        ]

        for item in buttons:
            wid = StyleButton(None, item[1])
            wid.set_type(item[2])

            layout.addWidget(wid)
            setattr(self, item[0], wid)


    def __cancel_handler(self):
        self.duplicate_option = False
        self.close()
    

    def __option_handler(self, index):
        self.duplicate_option = self.options.itemData(index)


    def set_data(self, data):
        self.__setup()

    def exec(self):
        super().exec()

        return self.duplicate_option


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


