from PyQt5 import QtCore

from .TorrentUI import TorrentUI

from Utility.Core import ACTIONS, STATES


# Torrent setting Control class
class TorrentControl(TorrentUI):

    item_requested = QtCore.pyqtSignal(str, int)

    def __init__(self, parent, info_data):
        super().__init__(parent)

        self.info_data = info_data
        self.info_index = []

        self.current_item = None
        self.current_index = 0

        self.__connect_slots()
        self.__setup_timer()
        self.__setup()


    def __connect_slots(self):
        self.nameCombo.currentIndexChanged.connect(self.__name_changed)
        self.tab.item_changed.connect(self.__stack_change)

        self.fileOption.priority_changed.connect(self.__request_handler)
        self.settingOption.requested.connect(self.__request_handler)

        self.resumeBtn.clicked.connect(self.__resume_handler)
        self.closeBtn.clicked.connect(self.close)
    

    def __setup(self):
        data = []
        for info in self.info_data:
            data.append((info.name, info))
        
        if data:
            self.info_index.extend([x[1] for x in data])
            self.nameCombo.addItems([x[0] for x in data])

            self.__pause_option(False)
            
        self.__toggle_btn()


    def __stack_change(self, index):
        self.stackLayout.setCurrentIndex(index)

        self.__pause_option()
        self.current_index = index
        self.__pause_option(False)
        

    def __name_changed(self, index):
        self.current_item = self.info_index[index]
        self.__change_data()


    def __change_data(self):
            
        items = self.info_data[self.current_item]

        if items:
            for index, wid in enumerate(self.options.values()):
                wid.set_data(items[index])

            self.__toggle_btn()
                

            
    def __pause_option(self, state = True):
        wid = self.options.get(self.current_index)

        if wid and hasattr(wid, 'set_paused'):
            wid.set_paused(state)


    def __request_handler(self, action):
        _id = self.current_item._id
        self.item_requested.emit(_id, action)


    def __resume_handler(self):

        s = ACTIONS.RESUME
        if self.current_item and self.current_item.state not in [STATES.PAUSED, STATES.COMPLETED]:
                s = ACTIONS.PAUSE
                self.peerOption._reset()
        
        self.__request_handler(s)
        self.resumeBtn.setEnabled(False)
        QtCore.QTimer.singleShot(1000, self.__toggle_btn)

    
    def __toggle_btn(self):
        txt = 'Resume'
        s = False

        if self.current_item:
            s = True
            if self.current_item.state != STATES.PAUSED:
                txt = 'Pause'
        
        self.resumeBtn.setText(txt)

        self.resumeBtn.setEnabled(s)
        self.setFocus()
    

    def __check_torrent_state(self):
        if self.current_item:
            state = self.current_item.state != STATES.COMPLETED

            if self.isEnabled() != state:
                self.resumeBtn.setEnabled(state)
            

    def __setup_timer(self):
        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(self.__check_torrent_state)
        self.__timer.start(1000)


