from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt

from UI.Torrent.TorrentSetting.Components.Base.Base import BasePanel, Scroll
from UI.Torrent.TorrentSetting.Components.Base.Items import ScrollItem

from Utility.Core import TORRENT


# Widget for displaying torrent tracker data
class TrackersOption(BasePanel):
    
    def __init__(self, parent):
        super().__init__(parent, False, True)

        self.stats = {}
        self.widgets = {}
        self.__stash = []

        self._panels()
        self._items_list()

        
    def _panels(self):
        panelLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(panelLayout)

        panelLayout.setContentsMargins(0, 0, 0, 10)

        panels = {
            TORRENT.TRACKER.STATS.DHT : 'DHT',
            TORRENT.TRACKER.STATS.LSD : 'LSD',
            TORRENT.TRACKER.STATS.PEX : 'PeX'
        }

        default_text = "Not Working"
        c = 0
        w, h = 150, 120
        
        for name, txt in panels.items():
    
            wid = ScrollItem(self, txt, default_text)
            wid.set_align(Qt.AlignmentFlag.AlignHCenter)
            wid.set_bold(True)

            wid.setFixedHeight(h)

            panelLayout.addWidget(wid, 0, c)

            self.stats[name] = wid

            c += 1


    def _items_list(self):
        listLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(listLayout)

        self.mainLayout.setStretchFactor(listLayout, 1)

        scroll = Scroll(self)
        scroll._widget(False, True)


        widget = scroll.widget()
        
        self.list_layout = widget.layout()
        self.list_layout.addStretch()
            

        listLayout.addWidget(scroll)


    def update_items(self, trackers):

        for url, data in trackers.items():
            wid = self.widgets.get(url)

            if not wid:
                wid = self.__get_item()
                wid.set_name(url)

                self.widgets[url] = wid

            state = data[TORRENT.TRACKER.STATE]

            if wid.get_state() != state:
                wid.set_state(state)
        


    def __update_stats(self, stats):

        for stat, wid in self.stats.items():
            value = stats.get(stat)

            if value and value != wid.get_state():
                wid.set_state(value)


    def set_data(self, data):
        self._reset()
        super().set_data(data)

        self.__init_timer()


    def __init_timer(self):
        self.update_timer = QtCore.QTimer()
        self.update_timer.setInterval(700)
        self.update_timer.timeout.connect(self.__update_data)
        self.update_timer.start(100)


    def __update_data(self):
        
        if self.info_data and not self.paused:

            trackers_info = self.info_data

            self.__update_stats(trackers_info.get_stats())

            self.update_items(trackers_info.get_trackers())


    def _reset(self):

        if hasattr(self, 'update_timer'):
            self.update_timer.stop()

        self.info_data = None

        self.__clear_widgets()
        self.__reset_data()


    def __reset_data(self):

        for wid in self.stats.values():
            wid.set_state(TORRENT.TRACKER_STATE.NOT_WORKING)
            
        for wid in self.__stash:
            wid.set_state(TORRENT.TRACKER_STATE.NOT_WORKING)
            

    def __get_item(self):

        item = None

        if self.__stash:
            item = self.__stash.pop()
            item.setVisible(True)
        else:
            item = ScrollItem(self)
            item.set_tracker(True)
            self.__add_child(item)

        return item


    def __clear_widgets(self):

        keys = list(self.widgets.keys())

        for key in keys:
            child = self.widgets.pop(key)

            if child:
                self.__remove_child(child)


    def __add_child(self, child, index = -1):

        count = self.list_layout.count()

        if index < 0 or index > count - 1:
            index = count - 1

        self.list_layout.insertWidget(index, child)
            


    def __remove_child(self, child):
        child.setVisible(False)
        self.__stash.append(child)




