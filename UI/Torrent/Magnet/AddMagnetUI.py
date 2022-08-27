from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from UI.Base.Dialog.BaseDialog import Dialog
from UI.Base.Input.StyleTextArea import TextArea
from UI.Base.Button.StyledButton import StyleButton

from Utility.Core import ICONS


# Torrent / Magnet link add dialog -- UI class



class AddMagnetUI(Dialog):

    def __init__(self, parent):
        super().__init__(parent, ICONS.DIALOGS.MAGNET)


        title = "Add Magnet/Torrent"
        self.setWindowTitle(title)
        
        w, h = 400, 150
        self.setMinimumWidth(w)
        self.setMaximumHeight(h)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self._input()
        self.mainLayout.addStretch()
        self._buttons()

        name = 'panel'
        self.setObjectName(name)

        self.__apply_style()


    def _input(self):

        inputLayout = QtWidgets.QVBoxLayout()
        inputLayout.setContentsMargins(0, 5, 0, 25)
        self.mainLayout.addLayout(inputLayout)

        text = 'Enter Path Or Magnet Link...'
        self.linkBox = TextArea()
        self.linkBox.setPlaceholderText(text)

        inputLayout.addWidget(self.linkBox)

    

    def _buttons(self):
        btnLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(btnLayout)

        buttons = [
            ('cancelBtn', 'Cancel', True),
            None,
            ('browseBtn', 'Browse', True),
            ('okBtn', 'OK', False),
        ]


        for item in buttons:
            if item:
                wid = StyleButton('', item[1])
                wid.setEnabled(item[2])
                btnLayout.addWidget(wid)

                setattr(self, item[0], wid)
            
            else:
                btnLayout.addStretch(1)

        
    
    def __apply_style(self):
        style = '''
        #panel {
            background-color : white;
        }
        '''

        self.setStyleSheet(style)


