
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
        
        name = 'auth-box'
        self.setObjectName(name)


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





