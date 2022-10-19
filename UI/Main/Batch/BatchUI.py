
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from UI.Base.Dialog.BaseDialog import Dialog
from UI.Base.Input.StyleTextArea import TextArea
from UI.Base.Button.StyledButton import StyleButton
from UI.Base.CheckBox.StyledCheckBox import CheckBox

from UI.Main.Boxes.Auth.AuthControl import AuthControl

from Utility.Core import ICONS
from Utility.Gui import get_icon

from .Components.Control.UIControl import UIControl


# Batch dialog -- UI class
class BatchUI(Dialog):
    def __init__(self, parent):
        super().__init__(parent, ICONS.DIALOGS.BATCH)
        
        w, h = 500, 300
        name = 'batch-dialog'
        title = "New Batch Download"
        
        self.setWindowTitle(title)
        self.setObjectName(name)
        self.resize(w, h)
        
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)


        self._header()
        self._content()
        self.mainLayout.addStretch()
        self._buttons()
        


    def _header(self):
        self.headLayout = QtWidgets.QHBoxLayout()
        self.headLayout.setContentsMargins(0, 5, 0, 15)
        self.mainLayout.addLayout(self.headLayout)

        self.__head_label()
        self.headLayout.addStretch()
        self.__info_icon()


    def __head_label(self):
        layout = QtWidgets.QHBoxLayout()
        self.headLayout.addLayout(layout)

        text = 'Batch Download'
        name = 'dialog-header'

        label = QtWidgets.QLabel(text)
        label.setObjectName(name)

        layout.addWidget(label)


    def __info_icon(self):
        layout = QtWidgets.QHBoxLayout()
        self.headLayout.addLayout(layout)

        icon_name = ICONS.OTHER.INFO
        s = 12

        name = 'tip-icon'
        text  = "<p>Add group of sequential file names like img001.jpg, img002.jpg, etc.<br>" + \
                "<b>Use the asterisk(*) wildcard</b> for the file name pattern.<br><br> For Example: http://www.ProGet.com/picture/img*.jpg </p>"


        label = QtWidgets.QLabel()
        label.setObjectName(name)

        label.setPixmap(get_icon(icon_name).pixmap(s, s))
        label.setToolTip(text)

        layout.addWidget(label)


    def _content(self):
        self.conLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.conLayout)

        self.__url_box()
        self.__control()
        self.__sample()
        self.__check()
        self.__auth()


    def __url_box(self):
        boxLayout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(boxLayout)

        text = 'Enter URL...'
        self.urlBox = TextArea()
        self.urlBox.setPlaceholderText(text)

        boxLayout.addWidget(self.urlBox)


    def __control(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 15, 0, 10)
        self.conLayout.addLayout(layout)

        self.control = UIControl()

        layout.addWidget(self.control)


        
    def __sample(self):
        layout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(layout)

        name = 'sample-box'
        self.empty_text = 'No wildcard (*) character in URL'

        self.sample_label = QtWidgets.QLabel(self.empty_text)
        self.sample_label.setObjectName(name)

        self.sample_label.setWordWrap(True)

        layout.addWidget(self.sample_label)



    def __check(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 10, 0, 5)
        self.conLayout.addLayout(layout)

        checks = [
            ('advanceCheck', 'Advanced'),
            None
        ]

        for item in checks:
            if item:
                wid = CheckBox(item[1], False)

                layout.addWidget(wid)
                setattr(self, item[0], wid)

            else:
                layout.addStretch()


    def __auth(self):
        authLayout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(authLayout)

        self.auth = AuthControl()
        self.auth.setVisible(False)

        authLayout.addWidget(self.auth)


    def _buttons(self):
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addLayout(btnLayout)

        data = [
            None,
            ('okBtn', 'OK'),
            ('cancelBtn', 'CANCEL')
        ]

        for item in data:
            if item:
                wid = StyleButton('', item[1])

                btnLayout.addWidget(wid)

                setattr(self, item[0], wid)
            else:
                btnLayout.addStretch(1)


