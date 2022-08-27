from PyQt5 import QtWidgets

from UI.Base.Dialog.Frameless.Base import FrameLessUI
from UI.Base.Button.StyledButton import StyleButton
from UI.Base.Input.StyleTextArea import TextArea

from Utility.Core import SELECTORS

class TextEntry(FrameLessUI):
    
    def __init__(self, parent):
        super().__init__(parent)

        self.text = ''

        w, h = 450, 200
        self.resize(w, h)

        self._area()
        self.mainLayout.addStretch(1)
        self._buttons()



    def _area(self):
        layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(layout)

        self.text_input = TextArea()

        layout.addWidget(self.text_input)

    
    def _buttons(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)

        buttons = [
            None,
            ('cancelBtn', 'CANCEL', self.close),
            ('updateBtn', 'UPDATE', self.__update_text),
        ]

        for item in buttons:
            if item:
                btn = StyleButton(None, item[1])
                btn.clicked.connect(item[2])
                layout.addWidget(btn)
                setattr(self, item[0], btn)
            else:
                layout.addStretch()



    def set_data(self, data):

        if data:
            self.text_input.set_text(data)



    def __update_text(self):
        new_text = self.text_input.text()
        self.text = new_text

        self.close()
    

    def exec(self):
        super().exec()

        return self.text











