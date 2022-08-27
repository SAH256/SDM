
from PyQt5 import QtWidgets

from UI.Base.Button.StyledButton import StyleButton


# Torrent metadata handler in add dialog -- UI class
class TorrentUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self._status()
        self._buttons()

        self.mainLayout.setContentsMargins(0, 10, 0, 10)


    def _status(self):
        statusLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(statusLayout, 1)

        text = '0/0'
        self.fileCount = QtWidgets.QLabel(text)

        statusLayout.addWidget(QtWidgets.QLabel('Files:'))
        statusLayout.addWidget(self.fileCount)

        statusLayout.addStretch(1)


    def _buttons(self):
        btnLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(btnLayout)

        btns = [
            ('selectFile', '', 'Select Files'),
        ]

        for name, icon, text in btns:
            wid = StyleButton(icon, text)
            wid.setEnabled(False)
            btnLayout.addWidget(wid)

            setattr(self, name, wid)

