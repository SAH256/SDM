from PyQt5 import QtCore
from .ControlUI import ControlUI


# Batch dialog, replacement control -- UI class
class UIControl(ControlUI):

    valueChanged = QtCore.pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.start = None
        self.stop = None
        self.zero_fill = None

        self.__connect_slots()
    

    def __connect_slots(self):
        self.optionCombo.currentIndexChanged.connect(self.__stack_handler)
        self.optionCombo.currentIndexChanged.connect(self.__change_handler)
        
        self.startBox.valueChanged.connect(self.__start_handler)
        self.stopBox.valueChanged.connect(self.__stop_handler)
        self.cardBox.valueChanged.connect(self.__zero_handler)

        self.firstChar.textChanged.connect(self.__start_handler)
        self.lastChar.textChanged.connect(self.__stop_handler)

        self.__change_handler(0)


    def get_info(self):
        start = self.start
        stop = self.stop

        if start > stop:
            temp = start
            start = stop
            stop = temp

        return [start, stop, self.zero_fill]



    def __start_handler(self, value):
        self.start = value
        self.__send_signal()


    def __stop_handler(self, value):
        self.stop = value
        self.__send_signal()


    def __zero_handler(self, value):
        self.zero_fill = value
        self.__send_signal()


    def __stack_handler(self, index):
        self.stackLayout.setCurrentIndex(index)


    def __change_handler(self, index):
        
        start, stop, zero = [None] * 3

        if index == self.NUMBER_INDEX:
            start = self.startBox.get_value()
            stop = self.stopBox.get_value()
            zero = self.cardBox.get_value()
        else:
            start = self.firstChar.text()
            stop = self.lastChar.text()
            zero = 0

        self.start = start
        self.stop = stop
        self.zero_fill = zero

        self.__send_signal()


    def __send_signal(self):
        self.valueChanged.emit(self.get_info())

