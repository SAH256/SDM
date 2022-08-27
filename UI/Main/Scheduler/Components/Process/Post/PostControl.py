from PyQt5.QtWidgets import QFileDialog

from Utility.Core import QUEUE

from .PostUI import PostUI


# Widget for controlling post-process of a queue - Control class
class PostProcess(PostUI):

    def __init__(self):
        super().__init__()

        self.__connect_slots()


    def __connect_slots(self):
        p = QUEUE.PROCESS.POST

        wid = self.widgets.get(p.OPEN_FILE)
        wid.toggled.connect(self.__toggle_file)

        wid = self.widgets.get(p.TURN_OFF)
        wid.toggled.connect(self.__toggle_options)

        self.options.currentIndexChanged.connect(self.__warning_handler)
        self.browseBtn.clicked.connect(self.__browse_handler)


    def __toggle_file(self, s):
        self.browseBtn.setEnabled(s)


    def __toggle_options(self, s):
        self.options.setEnabled(s)
        wid = self.widgets[QUEUE.PROCESS.POST.FORCE_SHUT_DOWN]
        wid.setEnabled(s)


    def __browse_handler(self):
        d = QFileDialog.getOpenFileName(caption = 'Select a file')

        if d:
            self.dirInput.setText(d[0])


    def get_data(self):
        p = QUEUE.PROCESS.POST

        data = {}

        for key, wid in self.widgets.items():
            data[key] = wid.isChecked()

        if data[p.OPEN_FILE]:
            data[p.OPEN_FILE] = self.dirInput.text()

        if data[p.TURN_OFF]:
            data[p.TURN_OFF] = self.options.currentText()
        else:
            data[p.FORCE_SHUT_DOWN] = False

        return data


    def set_data(self, data):

        self.__reset()

        for key, value in data.items():
            wid = self.widgets[key]

            wid.setChecked(bool(value))

        p = QUEUE.PROCESS.POST

        if data[p.OPEN_FILE]:
            self.dirInput.setText(data[p.OPEN_FILE])

        if data[p.TURN_OFF]:
            self.options.setCurrentText(data[p.TURN_OFF])


    def __reset(self):

        for wid in self.widgets.values():
            wid.setChecked(False)

        self.dirInput.clear()
        self.options.setCurrentIndex(0)


    def __warning_handler(self, index):

        visible = False

        if index:
            visible = True

        self.msgLabel.setVisible(visible)


