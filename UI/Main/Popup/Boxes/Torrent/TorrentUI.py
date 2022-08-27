
from PyQt5 import QtWidgets

from UI.Base.Dialog.Frameless.Base import FrameLessUI
from UI.Torrent.TorrentSetting.Components.File.FileControl import FileControl


class TorrentFile(FrameLessUI):

    def __init__(self, parent):
        super().__init__(parent)

        w, h = 600, 600
        self.resize(w, h)

        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self._content()
        


    def _content(self):
        layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(layout)
        self.mainLayout.setStretchFactor(layout, 5)

        self.torrent_manager = FileControl()

        layout.addWidget(self.torrent_manager)


    def set_data(self, data):
        self.torrent_manager.set_data(data)












