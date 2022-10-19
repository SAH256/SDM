
from PyQt5.QtCore import pyqtSignal

from .InterfaceUI import InterfaceUI


class Interface(InterfaceUI):
    
    style_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.interface_data = None
    
    
    def set_data(self, data):
        self.interface_data = data

        self.__setup()


    def __setup(self):
        self.iconCombo.addItems(self.interface_data.asset_pack_names())
        self.iconCombo.setCurrentText(self.interface_data.current_icon_pack())

        self.themeCombo.addItems(self.interface_data.theme_names())
        self.themeCombo.setCurrentText(self.interface_data.current_theme())

        self.langCombo.addItems(self.interface_data.lang_names())
        self.langCombo.setCurrentText(self.interface_data.current_lang())


    def apply_changes(self):
        need_exit = False
        new_theme = self.themeCombo.currentText()
        
        if self.interface_data.current_theme() != new_theme:
            self.interface_data.set_theme(new_theme)
            self.style_changed.emit()
        
        return need_exit
