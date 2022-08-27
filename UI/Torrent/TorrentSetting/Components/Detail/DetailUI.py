from PyQt5 import QtCore

from Utility.Core import TORRENT
from Utility.Util import sizeChanger
from Utility.Gui import find_links, get_transfer_str

from UI.Torrent.TorrentSetting.Components.Base.Base import Scroll
from UI.Torrent.TorrentSetting.Components.Base.Items import ScrollItem


# Widget for displaying a torrent detail data
class DetailOption(Scroll):

    def __init__(self):
        super().__init__()

        self.detail_data = None

        self.controls = {}
        self.paused = True
        
        self._widget(True, False)
        

        self._create_info_cells()

        
    
    def _create_info_cells(self):

        # hand code some of them for manipulating data
        items = [
            (TORRENT.DETAIL.HASH,           'HASH',                  True, (0, 0, 1, 2)),
            (TORRENT.DETAIL.NAME,           'NAME',                  True, (1, 0, 1, 2)),
            (TORRENT.DETAIL.SAVE_PATH,      'STORAGE PATH',          True, (2, 0, 1, 2)),
            (TORRENT.DETAIL.FILE_COUNT,     'NUMBER OF FILES',       True, (3, 0, 1, 1)),
            ('total_size',                  'FILE SIZE',             True, (3, 1, 1, 1)),
            ('speed_limit',                 'SPEED LIMIT',           True, (4, 0, 1, 2)),
            (TORRENT.DETAIL.DATE_COMPLETED, 'DATE COMPLETED',        True, (5, 0, 1, 1)),
            (TORRENT.DETAIL.DATE_ADDED,     'DATE ADDED',            True, (5, 1, 1, 1)),
            (TORRENT.DETAIL.TORRENT_DATE,   'TORRENT CREATION DATE', True, (6, 0, 1, 1)),
            (TORRENT.DETAIL.LAST_SEEN,      'LAST SEEN COMPLETE',    True, (6, 1, 1, 1)),
            ('comment_box',                 'COMMENT',               True, (7, 0, 1, 2)),
        ]

        temp_obj = TORRENT.DETAIL()

        

        for item in items:
            wid = ScrollItem(item[1], '', item[2])

            self.mainLayout.addWidget(wid, *item[3])

            setattr(self, item[0], wid)

            self.controls[item[0]] = wid
    


    def set_paused(self, state):
        self.paused = state


    def set_data(self, data):

        self.detail_data = data
        self._reset()
        self.__init_timer()
    

    def __init_timer(self):
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.__update_info)
        self.update_timer.setInterval(1000)
        self.update_timer.start(100)



    def __update_info(self):


        if self.detail_data and not self.paused:
            detail = self.detail_data

            for key, wid in self.controls.items():
                data = getattr(detail, key, None)
                if data:
                    wid.set_state(str(data).strip())


            txt = sizeChanger(detail.file_size)
            self.total_size.set_state(txt)

            txt = get_transfer_str(detail.down_limit, detail.up_limit)
            self.speed_limit.set_state(txt)
            

            if not self.comment_box.get_state():
                text = find_links(detail.comment)
                self.comment_box.set_state(text)


    def _reset(self):
        for wid in self.controls.values():
            wid.set_state('')
            



