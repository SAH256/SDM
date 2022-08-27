
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from UI.Base.Dialog.Frameless.Base import FrameLessUI
from UI.Base.CheckBox.StyledCheckBox import CheckBox
from UI.Base.Button.StyledButton import StyleButton
from UI.Base.Label.AnimLabel import AnimLabel

from Utility.Core import ICONS, SELECTORS


class Delete(FrameLessUI):

    def __init__(self, parent):
        super().__init__(parent)

        self.result_data = [False, False]

        w, h = 500, 300
        self.resize(w, h)
        
        self._content()
        self._buttons()

        self.__connect_slots()
        self.__style()



    def __connect_slots(self):
        self.cancelBtn.clicked.connect(self.close)
        self.proceedBtn.clicked.connect(self.__proceed_handler)


    def __setup(self, names, is_finished = False):

        message_text = 'Are you sure you want to remove finished tasks?'

        if is_finished:
            self.message.setText(message_text)

        if names:
            scroll_text = '\n'.join(filter(lambda x : type(x) == str, names))

            self.scroll_label.setText(scroll_text)
    

    def _content(self):
        self.conLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.conLayout, 5)

        self.__icon()
        self.__info()


    def __icon(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 0, 20, 0)
        self.conLayout.addLayout(layout)

        self.icon = AnimLabel(ICONS.ANIMATION.DOT_TABLE, loading = True)
        self.icon.start()

        layout.addWidget(self.icon, Qt.AlignmentFlag.AlignCenter)


    def __info(self):
        self.infoLayout = QtWidgets.QVBoxLayout()
        self.conLayout.addLayout(self.infoLayout)
        self.conLayout.setStretchFactor(self.infoLayout, 2)

        self.__label()
        self.__scroll()
        self.infoLayout.addStretch(1)
        self.__checks()




    def __label(self):
        layout = QtWidgets.QHBoxLayout()
        self.infoLayout.addLayout(layout)

        text = 'Are you sure you want to delete selected file(s)?'
        name = 'message'

        self.message = QtWidgets.QLabel(text)
        self.message.setObjectName(name)

        layout.addWidget(self.message)

    
    def __scroll(self):
        layout = QtWidgets.QHBoxLayout()
        self.infoLayout.addLayout(layout, 5)

        scroll = QtWidgets.QScrollArea()
        scroll.setFrameShape(scroll.Shape.NoFrame)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        name = 'scroll'

        self.scroll_label = QtWidgets.QLabel()
        self.scroll_label.setWordWrap(True)
        self.scroll_label.setObjectName(name)

        scroll.setWidget(self.scroll_label)

    
    def __checks(self):
        layout = QtWidgets.QGridLayout()
        self.infoLayout.addLayout(layout, 1)

        checks = [
            ('diskCheck', 'From storage as well', True),
        ]

        row = 0
        col = 0

        for name, text, d in checks:
            wid = CheckBox(text, False)
            wid.setEnabled(d)

            layout.addWidget(wid, row, col)
            setattr(self, name, wid)

            col += 1

            if col == 2:
                row += 1
                col = 0



    def _buttons(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout, 1)
        
        buttons = [
            ('cancelBtn', 'CANCEL', None),
            ('proceedBtn', 'PROCEED', SELECTORS.STATES.DANGER),
        ]

        for item in buttons:
            wid = StyleButton(None, item[1])

            if item[2]:
                wid.set_type(item[2])

            layout.addWidget(wid)
            setattr(self, item[0], wid)


    def set_data(self, data):
        names = data[0]
        is_finished = data[1]


        self.__setup(names, is_finished)


    def __proceed_handler(self):
        self.result_data = [True, self.diskCheck.isChecked()]
        self.close()


    def exec(self):
        super().exec()

        return self.result_data



    def __style(self):
        message_style = '''
        #message {
            font-size : 16px;
            color : red;
        }
        '''

        scroll_style = '''
        #scroll {
            background-color : white;
            color : #555;

            font-size : 12px;

        }
        '''

        self.message.setStyleSheet(message_style)
        self.scroll_label.setStyleSheet(scroll_style)





