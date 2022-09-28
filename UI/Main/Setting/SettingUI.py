from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from UI.Base.Dialog.BaseDialog import Dialog
from UI.Base.Button.StyledButton import StyleButton
from UI.Main.Tab.Option.InfiniteControl import InfiniteControl

from Utility.Core import SELECTORS, ICONS

from .Components.Interface.InterfaceUI import InterfaceUI
from .Components.Network.NetworkUI import NetworkUI
from .Components.Path.PathControl import Path
from .Components.Torrent.TorrentUI import TorrentUI



# App Setting dialog -- UI class
class SettingUI(Dialog):

    def __init__(self, parent):
        super().__init__(parent, ICONS.DIALOGS.SETTINGS)

        title = 'Application Setting'
        self.setWindowTitle(title)


        w, h = 600, 500
        self.resize(w, h)

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.options = {}

        self._tab()
        self._content()

        self.__add_tabs()

        name = 'panel'
        self.setObjectName(name)

        # self.__apply_style()
    

    def _tab(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout, 1)
        
        _dir = QtWidgets.QBoxLayout.Direction

        self.tab = InfiniteControl(self, _dir.TopToBottom, False)
        
        layout.addWidget(self.tab, 1, Qt.AlignmentFlag.AlignVCenter)



    def _content(self):
        self.conLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.conLayout, 8)
        self.mainLayout.setStretchFactor(self.conLayout, 8)

        self.__stack()
        self.__buttons()


    def __stack(self):
        self.stackLayout = QtWidgets.QStackedLayout()
        self.conLayout.addLayout(self.stackLayout, 9)
    

    def __buttons(self):
        layout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(layout)

        buttons = [
            None,
            ('closeBtn', 'CLOSE', None),
            ('applyBtn', 'APPLY', SELECTORS.STATES.CONFIRM),
        ]

        for item in buttons:
            if item:
                wid = StyleButton(None, item[1])
                wid.set_type(item[2])

                layout.addWidget(wid)
                setattr(self, item[0], wid)
            else:
                layout.addStretch()



    def __add_tabs(self):
    
        widgets = {
            'interfaceOption'  : ('INTER_INDEX',   ICONS.SETTING.INTERFACE,  'Interface', InterfaceUI),
            'networkOption'    : ('NETWORK_INDEX', ICONS.SETTING.NETWORK,  'Network',   NetworkUI),
            'pathOption'       : ('PATH_INDEX',    ICONS.SETTING.PATH,    'Path',      Path),
            'torrentOption'    : ('TORRENT_INDEX', ICONS.SETTING.TORRENT, 'Torrent',   TorrentUI),
            'pluginsOption'    : ('PLUGIN_INDEX',  ICONS.SETTING.PLUGIN,    'Plugins',   QtWidgets.QWidget),
        }


        for name, item in widgets.items():
            
            wid = item[3]()
            index = self.stackLayout.addWidget(wid)

            self.tab.add_item(item[1], item[2])

            self.options[index] = wid

            setattr(self, name, wid)
            # setattr(self, item[0], index)


    def __apply_style(self):
        style = '''

        #panel {
            background-color : white;
        }

        #label {
            font-family : Arial;
            font-size : 20px;
            font-weight : 900;
            color : #4523fe;
        }

        '''

        self.setStyleSheet(style)





