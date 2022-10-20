import time

from PyQt5.QtCore import QTimer

from UI.Torrent.TorrentSetting.Components.Base.Base import BasePanel
from UI.Torrent.TorrentSetting.Components.Base.Items import PeerItem
from UI.Torrent.TorrentSetting.Components.Base.List import ListItemView


# Widget for displaying torrent peer data
class PeerView(BasePanel):
    
    def __init__(self, parent):
        super().__init__(parent, False, True)

        self._list()
        self.__timer()


    def _list(self):
        wid = PeerItem(self)
        wid.setVisible(False)
        self.peer_list = ListItemView(self, wid, True)
        
        self.mainLayout.addWidget(self.peer_list)


    def set_paused(self, state):
        super().set_paused(state)
        
        self.peer_list.set_paused(state)


    def set_data(self, data):
        self._reset()
        super().set_data(data)


    def _reset(self):
        self.peer_list._reset()
        self.info_data = None
    
    
    def __timer(self):
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.__update_peers)
        self.update_timer.start(500)


    def __update_peers(self):
        if self.info_data and not self.paused:
            self.peer_list.update_data(self.info_data.get_peers())


