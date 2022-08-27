
from PyQt5.QtWidgets import QFileDialog

from Utility.Core import QUEUE

from .SubUI import SubUI


# Widget for controlling sub-process of a queue - Control class
class SubProcess(SubUI):

    def __init__(self):
        super().__init__()

        self.__connect_slots()


    def __connect_slots(self):
        s = QUEUE.PROCESS.SUB

        wid = self.widgets.get(s.MOVE_DIR)
        wid.toggled.connect(self.__toggle_dir)

        self.browseBtn.clicked.connect(self.__browse_handler)


    def __toggle_dir(self, s):
        self.browseBtn.setEnabled(s)


    def get_data(self):
        data = {}

        for key, wid in self.widgets.items():
            data[key] = wid.isChecked()

        s = QUEUE.PROCESS.SUB

        data[s.MOVE_DIR] = self.dirInput.text() if data[s.MOVE_DIR] else False

        return data


    def set_data(self, data):

        self.__reset()

        for key, value in data.items():
            wid = self.widgets.get(key)

            wid.setChecked(bool(value))

        value = data.get(QUEUE.PROCESS.SUB.MOVE_DIR)
        self.dirInput.setText(value if value else '')


    def __reset(self):

        for wid in self.widgets.values():
            wid.setChecked(False)

        self.dirInput.clear()


    def __browse_handler(self):
        r = QFileDialog.getExistingDirectory(caption = 'Choose a path')

        if r:
            self.dirInput.setText(r)

