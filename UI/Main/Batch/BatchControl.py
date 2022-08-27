
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt

from .BatchUI import BatchUI


# Batch dialog -- Control class
class BatchControl(BatchUI):

    sendRequest = pyqtSignal(list)

    def __init__(self, parent):
        super().__init__(parent)

        w, h = 500, 400
        self.setMaximumSize(w, h)

        self.url_pattern = ''
        self.wildcard = '*'
        self.info_value = self.control.get_info()

        self.__connect_slots()


    def __connect_slots(self):
        self.urlBox.textChanged.connect(self.__url_changed)
        self.control.valueChanged.connect(self.__value_changed)

        self.advanceCheck.toggled.connect(self.__advance_handler)

        self.cancelBtn.clicked.connect(self.close)
        self.okBtn.clicked.connect(self.close)
        self.okBtn.clicked.connect(self.__action_handler)


    def set_link(self, link):
        if link:
            self.urlBox.setText(link)


    def __url_changed(self):
        url = self.urlBox.text()
        has_wildcard = url.count(self.wildcard)

        if has_wildcard:
            self.url_pattern = url

            self.__show_info()
        else:
            self.__reset()
    
        self.__enable_ok(has_wildcard)


    def __value_changed(self, data):
        self.info_value = data
        self.__show_info()


    def __show_info(self):
        start = self.info_value[0]
        zero_fill = self.info_value[2]
        text = ''
        new_value = ''

        if isinstance(start, int):
            new_value = str(start).zfill(zero_fill)
        else:
            new_value = start

        text = self.url_pattern.replace(self.wildcard, new_value)
        self.sample_label.setText(text)


    def __action_handler(self):

        url = self.url_pattern.replace(self.wildcard, '{}')
        st = self.info_value[0]
        end = self.info_value[1]
        zero = self.info_value[2]

        result = [url, *(self.info_value), self.auth.get_user(), self.auth.get_password()]

        self.sendRequest.emit(result)


    def __advance_handler(self, state):
        self.auth.setVisible(state)

    def __enable_ok(self, state):
        self.okBtn.setEnabled(state)

    def __reset(self):
        self.sample_label.setText(self.empty_text)







