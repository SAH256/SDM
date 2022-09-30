from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


from UI.Base.Menu.StyledMenu import StyleMenu

from Utility.Core import TORRENT, ICONS
from Utility.Util import sizeChanger

from .Base import BaseWidget, create_icon_label



# Base item for all items that is using in torrent setting
class BaseItem(BaseWidget):

    def __init__(self, shadow = False):
        super().__init__(False, True)

        if shadow:
            self.__shadow()
    

    def __shadow(self):
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 0)
        shadow.setColor(Qt.GlobalColor.lightGray)
            
        self.setGraphicsEffect(shadow)


# items that is using in status, detail and trackers
class ScrollItem(BaseItem):
    
    def __init__(self, first = '', second = '', copy = False, shadow = True):
        super().__init__(shadow)

        self.class_prop = 'css-class'
        self.bold_value = 'Bold'
        self.tracker_value = "tracker"

        self._create_labels(first, second)

        if copy:
            self._setup_menu()
        
        name = 'torrent-scroll-item'
        self.setObjectName(name)


    def _create_labels(self, text_1, text_2):
        cell = [
            ('name', 'scroll-item-name', text_1),
            ('state', 'scroll-item-state', text_2)
        ]

        for item in cell:
            wid = QtWidgets.QLabel(item[2])
            wid.setWordWrap(True)
            wid.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
            wid.setOpenExternalLinks(True)
            wid.setObjectName(item[1])

            self.mainLayout.addWidget(wid)

            setattr(self, item[0], wid)
    


    def _setup_menu(self):
        self.MENU = StyleMenu()

        name = 'Copy'
        action = self.MENU.addAction(name)
        action.triggered.connect(self.__copy_handler)


    def __copy_handler(self):
        QtWidgets.QApplication.clipboard().setText(self.state.text())


    def set_align(self, value):
        self.mainLayout.setAlignment(self.name, value)
        self.mainLayout.setAlignment(self.state, value)


    def set_bold(self, state):
        name = ''
        if state:
            name = self.bold_value
        
        self.name.setProperty(self.class_prop, name)
        self.state.setProperty(self.class_prop, name)

        
        self.update()
    
    def set_tracker(self, state):
        name = ''
        if state:
            name = self.tracker_value
        
        self.name.setProperty(self.class_prop, name)
        self.state.setProperty(self.class_prop, name)
        
        self.update()

    
    def set_name(self, text):
        self.name.setText(text)
    
    def set_state(self, text):
        self.state.setText(text)
    
    def get_name(self):
        return self.name.text()
    
    def get_state(self):
        return self.state.text()


    def contextMenuEvent(self, ev):
        
        if hasattr(self, 'MENU'):
            self.MENU.popup(ev.globalPos())
        else:
            ev.ignore()

        super().contextMenuEvent(ev)



# items that is using in peer section
class PeerScrollItem(BaseItem):
    
    def __init__(self):
        super().__init__(True)

        self.prop_name = 'css-class'

        self.widgets = {}

        self._info_labels()
        self._create_monitors()
        
        name = 'peer-scroll-item'
        self.setObjectName(name)



    def _info_labels(self):
        infoLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(infoLayout)

        labels = [
            (TORRENT.PEER.CLIENT, 'N/A'),
            None,
            (TORRENT.PEER.PROGRESS, 'N/A %'),
        ]

        for item in labels:
            if item:
                wid = QtWidgets.QLabel(item[1])
                wid.setObjectName(item[0])

                infoLayout.addWidget(wid)
                self.widgets[item[0]] = wid
            else:
                infoLayout.addStretch(1)
            
            

    def _create_monitors(self):
        monLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(monLayout)

        text = "N/A"
        name = 'info'
        w = 70

        data = [
            (TORRENT.PEER.SPEED_DOWN, ICONS.OTHER.DOWN_ARROW),
            (TORRENT.PEER.SPEED_UP, ICONS.OTHER.UP_ARROW),
            1,
            (TORRENT.PEER.TOTAL_DOWN, ICONS.OTHER.TOTAL_DOWN),
            (TORRENT.PEER.TOTAL_UP, ICONS.OTHER.TOTAL_UP),
            2
        ]

        for item in data:
            if isinstance(item, int):
                monLayout.addStretch(item)
            else:
                wid = QtWidgets.QLabel(text)
                wid.setFixedWidth(w)
                wid.setObjectName(name)

                icon = create_icon_label(item[1])

                monLayout.addWidget(icon)
                monLayout.addWidget(wid, 1)

                self.widgets[item[0]] = wid


    def set_data(self, data):

        if data:
            for key, wid in self.widgets.items():
                value = data.get(key)

                if value :
                    if key.count('up') or key.count('down'):
                        value = sizeChanger(value)
                    elif key.count('progress'):
                        value = str(value) + ' %'
                    else:
                        value = str(value)
                        
                    wid.setText(value)

            is_seed = data[TORRENT.PEER.SEED]
            self.widgets[TORRENT.PEER.CLIENT].setProperty(self.prop_name, TORRENT.SEEDER if is_seed else TORRENT.LEECHER)
            
            self.update()
        

    def _reset(self):
        for wid in self.widgets.values():
            wid.setText('')




