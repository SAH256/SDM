from PyQt5 import QtCore

from .ChronoUI import ChronoUI
import datetime as dt


# Timer widget -- Control class
class ChronoControl(ChronoUI):

    toggled = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.__connect_slots()


    def __connect_slots(self):
        self.onCheck.toggled.connect(self.__enable_handler)


    def set_text(self, txt):
        if txt and isinstance(txt, str):
            self.onCheck.setText(txt)


    def __enable_handler(self, state):
        self.hour.setEnabled(state)
        self.minute.setEnabled(state)
        self.second.setEnabled(state)

        self.toggled.emit(state)


    def set_check(self, s):
        if s != None:
            self.onCheck.setChecked(s)

    def is_checked(self):
        return self.onCheck.isChecked()


    def get_data(self):
        if not self.is_checked():
            return None

        h = self.hour.get_value()
        m = self.minute.get_value()
        s = self.second.get_value()

        return dt.time(h, m, s).isoformat()


    def set_data(self, time_iso):

        s = False
        if time_iso:
            s = True

            time = dt.time.fromisoformat(time_iso)
            
            self.hour.set_value(time.hour)
            self.minute.set_value(time.minute)
            self.second.set_value(time.second)
        else:
            self.reset()

        self.set_check(s)


    def reset(self):
        t = dt.time(12, 0, 0)
        self.set_data(t.isoformat())



