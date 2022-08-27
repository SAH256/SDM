from PyQt5.QtCore import pyqtSignal

from UI.Base.Menu.StyledMenu import StyleMenu

from Utility.Core import TORRENT, ACTIONS

from .SettingUI import SettingUI


# Widget for displaying torrent setting -- Control class
class Setting(SettingUI):

    requested = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.__connect_slots()
        self.__enable_controls(False)
        self.__setup_force()
    

    def __connect_slots(self):

        [wid.toggled.connect(self.__data_changed_handler) for wid in self.options.values()]

        self.applyBtn.clicked.connect(self.__apply_handler)
        self.copyBtn.clicked.connect(self.__copy_link_handler)
        self.saveBtn.clicked.connect(self.__save_file_handler)


    def __setup_force(self):
        menu = StyleMenu()
        menu.triggered.connect(self.__force_handler)
        options = [TORRENT.REANNOUNCE, TORRENT.RECHECK]

        for option in options:
            menu.addAction(option)
        
        self.forceBtn.setMenu(menu)


    def __setup(self):
        if not self.info_data:
            return
        
        setting = self.info_data

        for _id, state in setting.options.items():
            wid = self.options.get(_id)
            wid.setChecked(state)
        
        self.sliders.set_up_limit(setting.get_up_limit())
        self.sliders.set_down_limit(setting.get_down_limit())


    def set_data(self, info_data):
        self.info_data = info_data
        
        self.__enable_controls(True)
        self.__setup()


    def __apply_handler(self):
        if not self.info_data:
            return

        setting = self.info_data

        down_limit = self.sliders.get_down_limit()
        up_limit = self.sliders.get_up_limit()

        setting.set_up_limit(up_limit)
        setting.set_down_limit(down_limit)

        for _id, wid in self.options.items():
            setting.set_option(_id, wid.isChecked())

        self.__toggle_apply()

        self.requested.emit(ACTIONS.SETTING)


    def __copy_link_handler(self):
        self.requested.emit(ACTIONS.COPY_LINK)


    def __save_file_handler(self):
        self.requested.emit(ACTIONS.SAVE_TORRENT)


    def __force_handler(self, action):
        request = ACTIONS.FORCE_REANNOUNCE

        if action.text() != TORRENT.REANNOUNCE:
            request = ACTIONS.FORCE_RECHECK
        
        self.requested.emit(request)


    def __data_changed_handler(self, data = None):
        self.__toggle_apply(True)


    def __enable_controls(self, state):
        # enable checkboxes
        for wid in self.options.values():
            wid.setEnabled(state)

        # enable other widgets
        for wid in self.widgets:
            wid.setEnabled(state)


    def __toggle_apply(self, state = False):
        self.applyBtn.setEnabled(state)


