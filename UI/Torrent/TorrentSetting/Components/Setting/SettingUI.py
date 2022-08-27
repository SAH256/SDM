from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from UI.Torrent.TorrentSetting.Components.Base.Base import BasePanel

from UI.Base.CheckBox.StyledCheckBox import CheckBox
from UI.Base.Button.StyledButton import StyleButton
from UI.Main.Boxes.SliderPane.PaneControl import PaneControl

from Utility.Core import TORRENT


# Widget for displaying torrent setting -- UI class
class SettingUI(BasePanel):
    
    def __init__(self):
        super().__init__(False, True)
        
        self.options = {}
        self.widgets = []
        
        self._content()
        self._btns()
    

    def _content(self):
        self.conLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(self.conLayout)

        self.__checks(0, 0)
        self.__sliders(0, 1)

        self.conLayout.setColumnStretch(0, 1)
        self.conLayout.setColumnStretch(1, 1)
    
    
    def __checks(self, row, column):
        layout = QtWidgets.QVBoxLayout()
        self.conLayout.addLayout(layout, row, column)
        
        for _id, text in TORRENT.OPTIONS.TEXTS.items():
            wid = CheckBox(text, False)
            
            layout.addWidget(wid)
            
            self.options[_id] = wid

        
        layout.addStretch()
        

    def __sliders(self, row, column):
        layout = QtWidgets.QVBoxLayout()
        self.conLayout.addLayout(layout, row, column)
        
        
        self.sliders = PaneControl()
        self.sliders.set_visible(False, up = True)

        self.widgets.append(self.sliders)

        layout.addWidget(self.sliders)
        layout.addStretch()


    def _btns(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)

        buttons = [
            ('forceBtn', 'Force'),
            ('copyBtn', 'Copy Magnet Link'),
            ('saveBtn', 'Save Torrent File'),
            ('applyBtn', 'Apply'),
        ]

        for item in buttons:
            wid = StyleButton(None, item[1])

            layout.addWidget(wid)
            self.widgets.append(wid)
            setattr(self, item[0], wid)


