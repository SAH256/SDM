from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

from UI.Torrent.TorrentSetting.Components.Base.Base import BasePanel
from UI.Torrent.TorrentSetting.Components.Base.Items import TrackerItem
from UI.Torrent.TorrentSetting.Components.Base.List import ListItemView


from Utility.Core import TORRENT


# Widget for displaying torrent tracker data
class TrackersOption(BasePanel):
    
    def __init__(self, parent):
        super().__init__(parent, False, True)

        self.stats = {}

        self._panels()
        self._list()
        
        self.__init_timer()
        

    def _panels(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)

        panels = {
            TORRENT.TRACKER.STATS.DHT : 'DHT',
            TORRENT.TRACKER.STATS.LSD : 'LSD',
            TORRENT.TRACKER.STATS.PEX : 'PeX'
        }

        default_text = "Not Working"
        h = 120
        
        for name, txt in panels.items():
    
            wid = TrackerItem(self, True)
            wid.setFixedHeight(h)
            wid.set_name(txt)
            wid.set_state(default_text)
            wid.set_tracker()

            layout.addWidget(wid)

            self.stats[name] = wid


    def _list(self):
        layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(layout)
        
        widget = TrackerItem(self)
        widget.setVisible(False)
        
        self.tracker_list = ListItemView(self, widget)
        
        layout.addWidget(self.tracker_list)


    def set_paused(self, state):
        super().set_paused(state)
        self.tracker_list.set_paused(state)
        

    def set_data(self, data):
        self._reset()
        super().set_data(data)


    def __update_stats(self, stats):

        for stat, wid in self.stats.items():
            value = stats.get(stat)

            if value and value != wid.get_state():
                wid.set_state(value)


    def __init_timer(self):
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.__update_data)
        self.update_timer.start(100)
        self.update_timer.setInterval(1000)


    def __update_data(self):
        if self.info_data and not self.paused:

            self.__update_stats(self.info_data.get_stats())
            self.tracker_list.update_data(self.info_data.get_trackers())


    def _reset(self):

        self.tracker_list._reset()

        self.info_data = None

        for wid in self.stats.values():
            wid.set_state(TORRENT.TRACKER_STATE.NOT_WORKING)

