from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from UI.Main.Tab.Option.InfiniteControl import InfiniteControl

from UI.Base.ComboBox.StyledComboBox import ComboBox
from UI.Base.Button.StyledButton import StyleButton
from UI.Base.Dialog.BaseDialog import Dialog

from Utility.Core import ICONS

from .Components.Status.StatusUI import StatusOption
from .Components.Detail.DetailUI import DetailOption
from .Components.File.FileControl import FileControl
from .Components.Tracker.TrackerUI import TrackersOption
from .Components.Peer.PeerUI import PeerOption
from .Components.Setting.SettingControl import Setting


# Torrent setting UI class
class TorrentUI(Dialog):

    def __init__(self, parent):
        super().__init__(parent, ICONS.DIALOGS.MAGNET)

        title = 'Torrent Setting'
        self.setWindowTitle(title)

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.options = {}

        w, h = 700, 500
        self.resize(w, h)

        self._tab()
        self._content()

        self.__add_tabs()

        self.__apply_style()
    


    def _tab(self):
        tabLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(tabLayout)

        _dir = QtWidgets.QBoxLayout.Direction

        self.tab = InfiniteControl(_dir.TopToBottom)

        tabLayout.addWidget(self.tab, 1, Qt.AlignmentFlag.AlignVCenter)
        tabLayout.addStretch(1)


    def _content(self):
        self.conLayout = QtWidgets.QVBoxLayout()
        self.conLayout.setContentsMargins(20, 0, 0, 0)
        self.mainLayout.addLayout(self.conLayout)
        self.mainLayout.setStretchFactor(self.conLayout, 2)

        self.__combo()
        self.__stack()
        self.__buttons()

    
    def __combo(self):
        comboLayout = QtWidgets.QHBoxLayout()
        comboLayout.setContentsMargins(0, 0, 0, 20)
        self.conLayout.addLayout(comboLayout)

        text = 'Torrent Name'
        label = QtWidgets.QLabel(text)

        self.nameCombo = ComboBox()

        comboLayout.addWidget(label)
        comboLayout.addWidget(self.nameCombo, 5)


    def __stack(self):
        self.stackLayout = QtWidgets.QStackedLayout()
        self.conLayout.addLayout(self.stackLayout)


    def __buttons(self):
        btnLayout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(btnLayout)

        buttons = [
            ('resumeBtn', 'Resume'),
            None,
            ('helpBtn', 'Help'),
            None,
            ('closeBtn', 'Close'),
        ]

        for item in buttons:
            if item:
                wid = StyleButton('', item[1])
                btnLayout.addWidget(wid)

                setattr(self, item[0], wid)

            else:
                btnLayout.addStretch()

    def __add_tabs(self):

        widgets = {
            'statusOption'  : ('STATUS_INDEX',  ICONS.TORRENT_SETTING.STATUS,  'Status',    StatusOption),
            'detailOption'  : ('DETAIL_INDEX',  ICONS.TORRENT_SETTING.DETAIL,  'Detail',    DetailOption),
            'fileOption'    : ('FILE_INDEX',    ICONS.TORRENT_SETTING.FILE,    'Files',     FileControl),
            'trackerOption' : ('TRACKER_INDEX', ICONS.TORRENT_SETTING.TRACKER, 'Trackers',  TrackersOption),
            'peerOption'    : ('PEER_INDEX',    ICONS.TORRENT_SETTING.PEER,    'Peer',      PeerOption),
            'settingOption' : ('SETTING_INDEX', ICONS.TORRENT_SETTING.SETTING, 'Setting',   Setting)
        }


        for name, item in widgets.items():
            
            wid = item[3]()
            index = self.stackLayout.addWidget(wid)

            self.tab.add_item(item[1], item[2])

            self.options[index] = wid

            setattr(self, name, wid)



    def __apply_style(self):
        style = '''
        QDialog {
            background-color : white;
        }
        '''

        self.setStyleSheet(style)




