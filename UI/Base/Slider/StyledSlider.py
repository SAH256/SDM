from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


# Slider style class
class Slider(QtWidgets.QWidget):
    
    def __init__(self, title, value, _min, _max, log_func = None):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.default = value
        self._min = _min
        self._max = _max
        self._log_func = log_func

        self._labels(title)
        self._slider()

        self.mainLayout.setContentsMargins(0, 0, 0, 0)


    def _labels(self, title):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)

        labels = [
            (None, title, 'slider-title'),
            ('log', '', None),
            None
        ]

        for item in labels:
            if item:
                wid = QtWidgets.QLabel(item[1])

                layout.addWidget(wid)

                if item[2]:
                    wid.setObjectName(item[2])

                if item[0]:
                    setattr(self, item[0], wid)

            else:
                layout.addStretch()


    def _slider(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)

        # just one widget it is not matter where we connect signals
        self.slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.slider.valueChanged.connect(self.__value_handler)

        self.slider.setValue(self.default)
        self.slider.setMinimum(self._min)
        self.slider.setMaximum(self._max)
        
        layout.addWidget(self.slider)

    def __value_handler(self, value):
        r = None

        if self._log_func:
            r = self._log_func(value)
        else:
            r = str(value)
            
        self.log.setText(r)


    def get_value(self):
        return self.slider.value()

    def set_value(self, value):
        self.slider.setValue(value)

    def _reset(self):
        self.slider.setValue(self.default)


