
from PyQt5 import QtWidgets

from UI.Base.Dialog.Frameless.Base import FrameLessUI
from UI.Base.Button.StyledButton import StyleButton
from UI.Base.Input.StyledInput import StyleInput

from Utility.Core import SELECTORS

class AddUI(FrameLessUI):
    
    def __init__(self, parent):
        super().__init__(parent)

        self.name = None
        self.exclude_list = None

        w, h = 300, 150
        self.resize(w, h)

        self._input()
        self.mainLayout.addStretch(1)
        self._buttons()
    

    def __setup(self, name):
        self.text_input.textChanged.connect(self.__name_handler)
        self.okBtn.clicked.connect(self.__ok_handler)
        self.cancelBtn.clicked.connect(self.close)

        self.text_input.setText(name)



    def _input(self):
        layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(layout)

        self.text_input = StyleInput()

        layout.addWidget(self.text_input)



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


    def set_data(self, data):
        self.exclude_list = data[1]

        name = f'{data[0]} #{len(data[1]) + 1}'

        self.__setup(name)
    

    def __name_handler(self, text):
        text = text.strip()
        btn_state = False

        if text and text not in self.exclude_list:
            btn_state = True
        
        self.__toggle_btn(btn_state)
    

    def __toggle_btn(self, state):
        self.okBtn.setEnabled(state)
    

    def __ok_handler(self):
        self.name = self.text_input.text().strip()
        self.close()

        


    def exec(self):
        super().exec()

        return self.name


