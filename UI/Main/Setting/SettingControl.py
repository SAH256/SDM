from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from .SettingUI import SettingUI


# App Setting dialog -- UI class
class Setting(SettingUI):

    def __init__(self, parent, setting_pack):
        super().__init__(parent)

        self.setting_pack = setting_pack

        self.__connect_slots()
        self.__setup()
    

    def __connect_slots(self):
        self.closeBtn.clicked.connect(self.close)
        self.applyBtn.clicked.connect(self.__apply_handler)
        self.tab.item_changed.connect(self.__stack_handler)
    
    def __setup(self):
        self.interfaceOption.set_data(self.setting_pack.get_interface())
        self.networkOption.set_data(self.setting_pack.get_network())
        self.pathOption.set_data(self.setting_pack.get_path())

    def __stack_handler(self, index):
        self.stackLayout.setCurrentIndex(index)


    def __apply_handler(self):
        for wid in self.options.values():
            if hasattr(wid, 'apply_changes'):
                wid.apply_changes()
                


