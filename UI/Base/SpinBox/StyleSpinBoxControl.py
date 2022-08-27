from PyQt5 import QtCore

from .StyledSpinBox import SpinBox
from UI.Base.Input.StyledInput import StyleInput


# Spin Box Control style class



class SpinBoxControl(SpinBox) :

    valueChanged = QtCore.pyqtSignal(int)

    def __init__(self, init_value = 0, min_value = 0, max_value = 100):
        super().__init__()

        self._min = 0
        self._max = 0
        self.value = 5
        self.z_fill = 1
        self.prev_value = -1

        self.set_range(min_value, max_value)
        self.set_value(init_value)
        self.default_width = self.width()

        self.__connect_slots()
    

    def __connect_slots(self):
        self.upBtn.clicked.connect(self.__increase_handler)
        self.numBox.textChanged.connect(self.__txt_handler)
        self.downBtn.clicked.connect(self.__decrease_handler)

        self.numBox.focusOutEvent = self.__input_focus_handler


    def get_value(self):
        return self.value


    def set_value(self, value):

        value = int(value)

        if (value != self.value) and (self._min <= value <= self._max):
            self.prev_value = self.value
            self.value = value

            self.__set_num(value)
            self.__toggle_btns()

            self.valueChanged.emit(value)



    def set_range(self, min_value, max_value):

        self.numBox.validator().setRange(min_value, max_value)
        self._min = min_value
        self._max = max_value


    def get_range(self):
        return range(self._min, self._max)
    
    def set_z_fill(self, z):
        if z > 0:
            self.z_fill = z
            self.__set_num(self.value)

    def __increase_handler(self):
        txt = self.numBox.text()

        if txt:
            txt = int(txt) + 1
        else:
            txt = self.value + 1

        self.set_value(txt)
        self.setFocus()


    def __decrease_handler(self):
        txt = self.numBox.text()

        if txt:
            txt = int(txt) - 1
        else:
            txt = self.value -1
        
        self.set_value(txt)
        self.setFocus()


    def __txt_handler(self, txt):

        if txt:
            value = int(txt)

            if self._min <= value <= self._max:
                self.set_value(value)
            else:
                self.numBox.setText(txt[:-1])


    def focusOutEvent(self, ev):
        super().focusOutEvent(ev)
        self.__set_num(self.value)



    def __input_focus_handler(self, ev):
        StyleInput.focusOutEvent(self.numBox, ev)
        self.__set_num(self.value)


    def __set_num(self, value):
        
        txt = str(value)

        if not self.numBox.hasFocus():
            txt = txt.zfill(self.z_fill)

        self.numBox.setText(txt)



    def __toggle_btns(self):
        self.upBtn.setEnabled(self.value < self._max)
        self.downBtn.setEnabled(self.value > self._min)


