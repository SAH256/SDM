
from PyQt5 import QtWidgets

from UI.Base.Button.StyledButton import StyleButton


# Torrent metadata handler in add dialog -- UI class
class TorrentUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setContentsMargins(0, 10, 0, 10)
        self.setLayout(self.mainLayout)

        self._status()
        self._buttons()
        
        name = 'torrent-box'
        self.setObjectName(name)



    def _status(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 0, 0, 0)
        self.mainLayout.addLayout(layout, 1)

        labels = [
            (None, 'Files:'),
            ('fileCount', '0/0'),
            None
        ]

        name = 'torrent-info'

        for item in labels:
            if item:
                wid = QtWidgets.QLabel(item[1])
                wid.setObjectName(name)
                
                layout.addWidget(wid)
                
                if item[0]:
                    setattr(self, item[0], wid)
            else:
                layout.addStretch(1)


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

