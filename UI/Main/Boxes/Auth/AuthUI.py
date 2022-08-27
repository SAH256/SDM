
from PyQt5 import QtWidgets

from UI.Base.Input.StyledInput import StyleInput


# Mini authentication input widget -- UI class
class AuthUI(QtWidgets.QGroupBox) :

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.mainLayout.setContentsMargins(5, 10, 5, 10)

        self._label()
        self._inputs()

        self.__apply_style()


    def _label(self):
        labelLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(labelLayout, 1)

        text = 'Use Authentication'
        self.setTitle(text)
        self.setCheckable(True)


    def _inputs(self):
        inputLayout = QtWidgets.QFormLayout()
        self.mainLayout.addLayout(inputLayout)

        inputLayout.setHorizontalSpacing(30)

        inputs = [
            ('username', 'Username', False),
            ('password', 'Password', True),
        ]

        for name, p, is_password in inputs:

            wid = StyleInput()
            wid.setPlaceholderText(p)

            if is_password:
                wid.setEchoMode(wid.EchoMode.Password)

            inputLayout.addRow(p, wid)

            setattr(self, name, wid)


    def __apply_style(self):
        style = '''
        QGroupBox {
            border: 1px solid lightgray;
            padding : 20px  2px 5px 2px;
            border-radius: 2px;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left; /* position at the top center */
            padding: 0 3px;
        }

        QGroupBox::indicator{
            border : 2px solid #4968f3;
            width : 11px;
            height : 11px;
            border-radius : 3px;
        }

        QGroupBox::indicator::checked {
            background-color : #4968f3;
            image : url(assets/Icons/Blue/Other/tick.svg);
        }


        QGroupBox::indicator::disabled {
            border-color : #aaa;
        }
        '''

        self.setStyleSheet(style)







