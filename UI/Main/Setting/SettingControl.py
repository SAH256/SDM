from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

from .SettingUI import SettingUI


# App Setting dialog -- UI class
class Setting(SettingUI):
    
    style_changed = pyqtSignal()

    def __init__(self, parent, setting_pack):
        super().__init__(parent)

        self.setting_pack = setting_pack
        self.need_exit = False

        self.__connect_slots()
        self.__setup()
    

    def __connect_slots(self):
        self.closeBtn.clicked.connect(self.close)
        self.applyBtn.clicked.connect(self.__apply_handler)
        self.tab.item_changed.connect(self.__stack_handler)
        
        self.interfaceOption.style_changed.connect(self.__style_handler)
    
    def __setup(self):
        self.interfaceOption.set_data(self.setting_pack.get_interface())
        self.networkOption.set_data(self.setting_pack.get_network())
        self.pathOption.set_data(self.setting_pack.get_path())

    def __stack_handler(self, index):
        self.stackLayout.setCurrentIndex(index)


    def __apply_handler(self):
        need_exit = False
        
        for wid in self.options.values():
            if hasattr(wid, 'apply_changes'):
                result = wid.apply_changes()
                
                need_exit = need_exit or result
        
        self.need_exit = need_exit


    def __style_handler(self):
        self.style_changed.emit()
        self.tab._refresh()


    def exec(self):
        super().exec()
        return self.need_exit
