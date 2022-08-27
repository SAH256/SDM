import time

from PyQt5 import QtWidgets, QtCore

from UI.Torrent.TorrentSetting.Components.Base.Base import BaseWidget, Scroll
from UI.Torrent.TorrentSetting.Components.Base.Items import PeerScrollItem


# Widget for displaying torrent peer data
class PeerOption(Scroll):

    def __init__(self):
        super().__init__()

        self.peer_data = None
        self.paused = True

        self.widgets = {}
        self.__stash = []
        
        self._widget(False, True)
        self.mainLayout.addStretch()


    def __init_timer(self):
        
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.__update_peers)
        self.update_timer.setInterval(700)
        self.update_timer.start(200)



    def set_data(self, data):
        self.peer_data = data

        self.__init_timer()


    def set_paused(self, state):

        self.paused = state

        if state:
            self._reset()


    def __update_peers(self):

        if self.peer_data and not self.paused:
            
            peers = self.peer_data.get_peers()

            old_keys = list(self.widgets.keys())
            new_keys = list(peers.keys())

            for key in old_keys:
                if key not in new_keys:

                    wid = self.widgets.pop(key)
                    self.__stash_child(wid)
            

            for ip, peer in peers.items():

                wid = self.widgets.get(ip)

                if not wid:
                    wid = self.__get_item()
                    self.widgets[ip] = wid
                
                wid.set_data(peer)


    def _reset(self):
        self.__remove_children()

    def __get_item(self):

        item = None

        if self.__stash:
            item = self.__stash.pop()
            item.setVisible(True)

        else:
            item = PeerScrollItem()
            self.__add_to_panel(item, 0)
        
        return item
            


    def __add_to_panel(self, widget, index = -1):

        count = self.mainLayout.count()

        if index < 0 or index > count - 1:
            index =  count - 1

        self.mainLayout.insertWidget(index, widget)

    
    def __stash_child(self, child):

        child.setVisible(False)
        child._reset()

        self.__stash.append(child)

    def __remove_children(self):
        keys = list(self.widgets.keys())

        for key in keys:
            child = self.widgets.pop(key)
            
            if child:
                self.__stash_child(child)
    
