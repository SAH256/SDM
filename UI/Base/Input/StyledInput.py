
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


# Single line text input style class



class StyleInput(QtWidgets.QLineEdit):
    
    def __init__(self):
        super().__init__()

        self.setAutoFillBackground(True)
        self.setClearButtonEnabled(True)

        self.prop_name = 'cssClass'
        self.class_name = 'double'
        
        self.__apply_style()


    # set double border property
    def set_double(self, state):
        name = ''
        if state:
            name = self.class_name
        
        self.setProperty(self.prop_name, name)


    def __apply_style(self):


        style = """

        QLineEdit {
            border : none;
            padding : 5px;
            background-color : #eee;
        }

        QLineEdit:disabled {
            color : #333;
            background-color : #ccc;
        }

        QLineEdit:disabled[text=""] {
            border-bottom : 2px solid red;
        }

        QLineEdit:focus {
            background-color : #fff;
            border-bottom : 2px solid blue;
        }

        QLineEdit[echoMode = "2"] {
             lineedit-password-character : 9679;
        }

        QLineEdit[cssClass="double"]:focus {
            border-top : 2px solid blue;
        }
        
        #error {
            border-bottom: 2px solid red;
        }

        #error:focus {
            border-bottom : 1px solid red;
        }

        """


        self.setStyleSheet(style)

    def setObjectName(self, name):
        super().setObjectName(name)

        self.__apply_style()

    
    def _reset(self):
        self.setText('')



