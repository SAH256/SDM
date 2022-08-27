from PyQt5 import QtWidgets, QtGui, QtCore

from Utility.Core import TORRENT
from Utility.Gui import get_transfer_str
from Utility.Util import sizeChanger
from Utility.Calcs import format_remain_time

from UI.Torrent.TorrentSetting.Components.Base.Base import BasePanel
from UI.Torrent.TorrentSetting.Components.Base.Items import ScrollItem



# Widget for displaying torrent status data
class StatusOption(BasePanel):
    
    def __init__(self):
        super().__init__(False, True)

        self.controls = {}

        self._panels()

        self.mainLayout.addStretch(1)
        

    def _panels(self):

        infoLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(infoLayout)

        items = [
            (TORRENT.STATUS.STATUS,       'STATUS'),
            ('speed',                     'SPEED'),
            (TORRENT.STATUS.UPLOADED,     'UPLOADED'),
            (TORRENT.STATUS.DOWNLOADED,   'DOWNLOADED'),
            (TORRENT.STATUS.ETA,          'ETA'),
            (TORRENT.STATUS.SHARE_RATIO,  'SHARE RATIO'),
            ('seeders_info',              'SEEDERS'),
            ('leechers_info',             'LEECHERS'),
            (TORRENT.STATUS.SEEDING_TIME, 'SEEDING TIME'),
            (TORRENT.STATUS.ACTIVE_TIME,  'ACTIVE TIME'),
            ('pieces_info',               'PIECES'),
            (TORRENT.STATUS.AVAILABILITY, 'AVAILABILITY'),
        ]


        row, col = 0, 0
        max_col = 2

        for item in items:

            wid = ScrollItem(item[1])
            infoLayout.addWidget(wid, row, col)

            setattr(self, item[0], wid)
            self.controls[item[0]] = wid
                
            col += 1

            if col == max_col:
                row += 1
                col = 0


    def __update_status(self):
        
        if self.info_data and not self.paused:

            status = self.info_data

            for key, wid in self.controls.items():
                if hasattr(status, key):
                    data = getattr(status, key)
                    wid.set_state(str(data))


            speed = get_transfer_str(status.down_speed, status.up_speed, True)
            self.speed.set_state(speed)
            self.uploaded.set_state(sizeChanger(status.uploaded))


            eta = 'Undefinded'

            if status.eta > -1:
                eta = format_remain_time(status.eta)

            self.eta.set_state(eta)
            

            down = sizeChanger(status.downloaded)
            total = sizeChanger(status.total_size)

            self.downloaded.set_state(f"{down} / {total}   ({status.progress * 100} %)")

            seeds = f"{status.seeders} ({status.total_seeds})"
            leechs = f"{status.leechers} ({status.total_peers - status.total_seeds})"

            self.seeders_info.set_state(seeds)
            self.leechers_info.set_state(leechs)


            total_pieces = status.total_pieces
            down_pieces = status.pieces
            piece_size = status.piece_size

            self.pieces_info.set_state(f"{down_pieces}/{total_pieces} ({sizeChanger(piece_size)})")
            

    def __init_timer(self):
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.__update_status)
        self.update_timer.setInterval(500)
        self.update_timer.start(300)


    def set_data(self, data):
        super().set_data(data)
        
        self.__init_timer()
        
    def _reset(self):
        for item in self.controls.values():
            item[0].set_state('')

