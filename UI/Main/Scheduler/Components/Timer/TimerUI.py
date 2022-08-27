
from PyQt5 import QtWidgets

from UI.Main.Boxes.Chrono.ChronoControl import ChronoControl
from UI.Main.Boxes.Date.DateControl import DateControl


# Timer setting widget in scheduler for a queue -- UI class
class TimerUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self._start()
        self._date()
        self._stop()

        self.mainLayout.addStretch(1)
        self.mainLayout.setSpacing(10)


    def _start(self):
        startLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(startLayout)

        txt = 'Start At:'
        self.start_timer = ChronoControl()
        self.start_timer.set_text(txt)

        startLayout.addWidget(self.start_timer)


    def _date(self):
        dateLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(dateLayout)

        self.date_option = DateControl()
        self.date_option.setEnabled(False)

        dateLayout.addWidget(self.date_option)


    def _stop(self):
        stopLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(stopLayout)

        txt = 'Stop At:'
        self.stop_timer = ChronoControl()
        self.stop_timer.set_text(txt)

        stopLayout.addWidget(self.stop_timer)





