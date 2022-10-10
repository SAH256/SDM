from PyQt5 import QtCore

from Utility.Core import ACTIONS
from Utility.Util import sizeChanger

from .FileUI import FileUI




# Widget for displaying Files in a torrent -- Control class
class FileControl(FileUI):
    
    priority_changed = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)

        self.total_size = 0
        self.total_count = 0
        
        self.__stash = []
        self.files = []

        self.__connect_slots()


    def __connect_slots(self):
        
        self.fileTable.setting_changed.connect(self.__change_handler)
        self.allCheck.stateChanged.connect(self.__all_handler)

        self.applyBtn.clicked.connect(self.__apply_handler)
        self.resetBtn.clicked.connect(self.__reset_handler)
        

    def __add_item(self, parent, item):
        self.fileTable._add_item(parent, item)


    def __init_timer(self):
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.__update_handler)
        self.update_timer.setInterval(700)
        self.update_timer.start(500)


    def set_data(self, data):
        super().set_data(data)

        self._reset()
        self.__init_timer()


    def __setup(self):

        file_info = self.info_data

        if file_info:
            
            item = file_info.main_folder

            if file_info.is_single_file():
                item = file_info.files[0]

            if item:
                self.__add_item(None, item)
                self.__change_handler()


    def set_size(self, size):
        if size >= 0:
            self.total_size = size
            
            
    def set_count(self, c):
        if c >= 0:
            self.total_count = c


    def _reset(self):
        if hasattr(self, 'update_timer'):
            self.update_timer.stop()
        
        self.fileTable._remove()
        

    def __show_info(self):
        txt = f"{sizeChanger(self.total_size)} ({self.total_count} file{'s' if self.total_count > 0 else ''})"
        self.infoLabel.setText(txt)


    def __change_handler(self, refresh = False):

        if self.info_data:

            if refresh:
                self.info_data.update_status()

            self.set_size(self.info_data.get_size())
            self.set_count(self.info_data.get_count())
        
            self.__show_info()

            self.__toggle_btn(True)
        

    def __all_handler(self, state):
        self.fileTable._select_all(state)


    def __apply_handler(self):
        self.fileTable._apply()

        if self.info_data:

            self.info_data.total_size = self.total_size
            self.priority_changed.emit(ACTIONS.PRIORITY)

        self.__change_handler(True)
        self.__toggle_btn()
    
    def __reset_handler(self):
        self.fileTable._reset(True)
        self.__change_handler(True)
        self.__toggle_btn()


    def __toggle_btn(self, state = False):
        
        self.applyBtn.setEnabled(state)
        self.resetBtn.setEnabled(state)
        

    def __update_handler(self):
        if self.info_data:
            if self.fileTable.hasItems():
                self.fileTable._update()
            else:
                if self.info_data.has_files():
                    self.__setup()
        


