
from PyQt5 import QtCore, QtWidgets

from UI.Main.Popup.PopupControl import create_popup

from Utility.Core import POPUP_TYPE

from .TorrentBox import TorrentUI


# Torrent metadata handler in add dialog -- UI class
class TorrentControl(TorrentUI):

    info_changed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.file_info = None

        self.__connect_slots()


    def __connect_slots(self):
        self.selectFile.clicked.connect(self.__select_file_handler)


    def set_data(self, info):
        self.file_info = info

        if info:
            self.__update_info()
            self.__enable_btn(True)


    def __enable_btn(self, state = False):
        self.selectFile.setEnabled(state)


    def __update_info(self):
        count = self.file_info.get_count()
        total = self.file_info.get_total_count()

        txt = f'{count}/{total}'

        self.set_count_text(txt)

        self.info_changed.emit()


    def set_count_text(self, text):
        self.fileCount.setText(text)


    def _reset(self):
        self.info = None
        self.__enable_btn()


    def __select_file_handler(self):
        _type = POPUP_TYPE.TORRENT_FILE
        title = 'Manage Torrent Files'
        
        create_popup(self, _type, title, None, self.file_info)

        self.__update_info()



