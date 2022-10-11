from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from Utility.Core import TORRENT, ICONS, SELECTORS
from Utility.Util import sizeChanger
from Utility.Structure.Setting import Interface

from .Base import BaseWidget, create_icon_label



# Base item for all items that is using in torrent setting
class BaseItem(BaseWidget):

    def __init__(self, parent, shadow = False):
        super().__init__(parent, False, True)

        self._labels()

        if shadow:
            self.__shadow()
    
    def _labels(self):
        cell = [
            ('name', 'item-id'),
            ('state', 'item-state')
        ]

        for item in cell:
            wid = QtWidgets.QLabel()
            wid.setObjectName(item[1])

            self.mainLayout.addWidget(wid)

            setattr(self, item[0], wid)


    def set_name(self, name):
        self.name.setText(name)

    def get_state(self):
        return self.state.text()


    def set_state(self, state):
        self.state.setText(state)
        
    def get_name(self):
        return self.name.text()
    
    def set_align(self, value):
        self.mainLayout.setAlignment(self.name, value)
        self.mainLayout.setAlignment(self.state, value)


    def set_bold(self, state):
        if not state:
            return
        
        name = SELECTORS.VALUE.BOLD
        self.name.setProperty(SELECTORS.PROPERTY.CSS_CLASS, name)
        self.state.setProperty(SELECTORS.PROPERTY.CSS_CLASS, name)

        self.update()

    def set_tracker(self):
        self.set_align(Qt.AlignmentFlag.AlignHCenter)
        self.set_bold(True)
        self.setProperty(SELECTORS.PROPERTY.CSS_CLASS, SELECTORS.VALUE.TRACKER)
        self.update()
    

    def __shadow(self):
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 0)
        shadow.setColor(QtGui.QColor(Interface.COLORS.get('CONTAINER-SHADOW')))
            
        self.setGraphicsEffect(shadow)


# items that is using in status, detail and trackers
class ScrollItem(BaseItem):
    
    def __init__(self, parent, first = '', second = '', copy = False, shadow = True):
        super().__init__(parent, shadow)

        self.set_name(first)
        self.set_state(second)
        
        if copy:
            self._setup_menu()
        
        name = 'scroll-item'
        self.setObjectName(name)


    def _labels(self):
        cell = [
            ('name', 'scroll-item-name'),
            ('state', 'scroll-item-state')
        ]

        for item in cell:
            wid = QtWidgets.QLabel()
            wid.setWordWrap(True)
            wid.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
            wid.setOpenExternalLinks(True)
            wid.setObjectName(item[1])

            self.mainLayout.addWidget(wid)

            setattr(self, item[0], wid)
    


    def _setup_menu(self):
        self.MENU = QtWidgets.QMenu(parent = self)

        name = 'Copy'
        action = self.MENU.addAction(name)
        action.triggered.connect(self.__copy_handler)

    def __copy_handler(self):
        QtWidgets.QApplication.clipboard().setText(self.state.text())

    def contextMenuEvent(self, ev):
        
        if hasattr(self, 'MENU'):
            self.MENU.popup(ev.globalPos())
        else:
            ev.ignore()

        super().contextMenuEvent(ev)



class TrackerItem(BaseItem):

    def __init__(self, parent, shadow = False):
        super().__init__(parent, shadow)

        name = 'tracker-item'
        self.setObjectName(name)


    def set_data(self, info_data):
        url = info_data.get(TORRENT.TRACKER.URL)
        state = info_data.get(TORRENT.TRACKER.STATE)
        
        self.set_name(url)
        self.set_state(state)
        


# items that is using in peer section
class PeerItem(BaseItem):
    
    def __init__(self, parent):
        self.widgets = {}
        super().__init__(parent, False)

        name = 'peer-item'
        self.setObjectName(name)


    def _labels(self):
        self._info_labels()
        self._create_monitors()


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
        name = 'peer-info'
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

                if key.count('up') or key.count('down'):
                    value = sizeChanger(value)
                elif key.count('progress'):
                    value = str(value) + ' %'
                else:
                    value = str(value)
                    
                wid.setText(value)

            is_seed = data[TORRENT.PEER.SEED]
            value = SELECTORS.VALUE.SEEDER if is_seed else SELECTORS.VALUE.LEECHER

            self.widgets[TORRENT.PEER.CLIENT].setProperty(SELECTORS.PROPERTY.CSS_CLASS, value)
            
            self.update()
    
    def update(self):
        wid = self.widgets[TORRENT.PEER.CLIENT]
        
        self.style().unpolish(wid)
        self.style().polish(wid)
        super().update()

    def _reset(self):
        for wid in self.widgets.values():
            wid.setText('')




