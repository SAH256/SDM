from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from UI.Base.CheckBox.StyledCheckBox import CheckBox
from UI.Base.Button.StyledButton import StyleButton

from UI.Torrent.TorrentSetting.Components.Base.Base import BasePanel

from .Components.Tree import View


# Widget for displaying Files in a torrent -- UI class
class FileUI(BasePanel):

    def __init__(self, parent):
        super().__init__(parent, False, True)

        self._header()
        self._content()
        self._footer()


    def _header(self):
        self.headerLayout = QtWidgets.QHBoxLayout()
        self.headerLayout.setContentsMargins(0, 5, 0, 15)
        self.mainLayout.addLayout(self.headerLayout)

        self.__labels()
        self.headerLayout.addStretch(1)
        self.__checks()


    def __labels(self):
        labelLayout = QtWidgets.QVBoxLayout()
        self.headerLayout.addLayout(labelLayout)

        labels = [
            ('file-message', 'Change priority for important files'),
        ]

        for item in labels:
            if item:
                wid = QtWidgets.QLabel(item[1])
                wid.setObjectName(item[0])

                labelLayout.addWidget(wid)


    def __checks(self):
        checkLayout = QtWidgets.QHBoxLayout()
        self.headerLayout.addLayout(checkLayout)
        self.headerLayout.setAlignment(checkLayout, Qt.AlignmentFlag.AlignBottom)

        checks = [
            ('allCheck', 'Select All')
        ]

        for item in checks:
            if item:
                wid = CheckBox(item[1], False)

                checkLayout.addWidget(wid, 1)

                setattr(self, item[0], wid)


    def _content(self):
        conLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(conLayout)

        self.fileTable = View()

        conLayout.addWidget(self.fileTable)


    def _footer(self):
        self.footerlayout = QtWidgets.QHBoxLayout()
        self.footerlayout.setContentsMargins(0, 15, 0, 5)
        self.mainLayout.addLayout(self.footerlayout)

        self.__info()
        self.footerlayout.addStretch(1)
        self.__buttons()


    def __info(self):
        infoLayout = QtWidgets.QHBoxLayout()
        self.footerlayout.addLayout(infoLayout)

        name = 'file-info'
        message = "No File Selected"
        self.infoLabel = QtWidgets.QLabel(message)
        self.infoLabel.setObjectName(name)

        infoLayout.addWidget(self.infoLabel)


    def __buttons(self):
        btnLayout = QtWidgets.QHBoxLayout()
        self.footerlayout.addLayout(btnLayout)

        btns = [
            ('resetBtn', 'Reset'),
            ('applyBtn', 'Apply'),
        ]

        for item in btns:
            if item:
                wid = StyleButton('', item[1])
                wid.setEnabled(False)
                btnLayout.addWidget(wid)

                setattr(self, item[0], wid)

