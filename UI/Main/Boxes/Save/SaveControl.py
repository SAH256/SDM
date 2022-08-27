import shutil as sh
import os

from PyQt5 import QtWidgets, QtCore

from Utility.Util import sizeChanger

from .SaveBox import SavePath


# Save path selector widget -- Control class
class SaveControl(SavePath):

    path_changed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.file_size = 0

        self.__connect_slots()


    def __connect_slots(self):
        self.save_box.textChanged.connect(self.__save_path_handler)
        self.browseBtn.clicked.connect(self.__path_select_handler)


    def set_path(self, path):

        if os.path.exists(path):
            self.save_box.setText(path)


    def get_path(self):
        return self.save_box.text()


    def set_size(self, size):
        self.file_size = size
        self.__change_info()


    def get_size(self):
        return self.file_size


    def __save_path_handler(self, path):

        if os.path.exists(path):
            self.__change_info()
        else:
            self.__reset_widgets()

        self.path_changed.emit()


    def __path_select_handler(self):
        text = 'Select New Path'
        path = QtWidgets.QFileDialog.getExistingDirectory(caption = text)

        if path:
            self.set_path(path)


    def __change_info(self):
        path = self.save_box.text()

        if not path:
            return

        info = sh.disk_usage(path)

        free = sizeChanger(info.free)
        total = sizeChanger(info.total)
        per = info.free * 100 // info.total

        self.free_space.setText(free)
        self.total_space.setText(total)
        self.percentage.setText(f'{per}%')

        color = self.OK

        if info.free < self.file_size:
            color = self.DANGER

        self.__change_color(color)


    def __change_color(self, name):
        for wid in self._widgets:
            wid.setObjectName(name)
            self.__update(wid)


    def __update(self, wid):
        self.style().unpolish(wid)
        self.style().polish(wid)


    def __reset_widgets(self):
        text = 'N/A'

        for wid in self._widgets:
            wid.setText(text)
            wid.setObjectName('')
            self.__update(wid)

