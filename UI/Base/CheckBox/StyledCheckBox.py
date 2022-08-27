from PyQt5 import QtWidgets


class CheckBox(QtWidgets.QCheckBox):
    
    def __init__(self, text, default = True):
        super().__init__(text)

        self.default = default

        self._reset()
        self.__apply_style()
    

    def _reset(self):
        self.setChecked(self.default)



    def __apply_style(self):

        style = '''
            QCheckBox::indicator{
                border : 2px solid #4968f3;
                width : 11px;
                height : 11px;
                border-radius : 3px;
            }

            QCheckBox::indicator::checked {
                background-color : #4968f3;
                image : url(assets/Icons/Default/Other/tick.svg);
            }

            QCheckBox::indicator::disabled {
                border-color : #aaa;
            }

            QCheckBox::indicator::disabled::checked {
                background-color : #aaa;
            }

        '''

        self.setStyleSheet(style)




        