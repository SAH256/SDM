
from PyQt5 import QtWidgets

from UI.Base.Slider.StyledSlider import Slider

from Utility.Util import sizeChanger


# Panel for handling sliders -- UI class
class PaneUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self._sliders()
    

    def _sliders(self):

        sliders = [
            ('partSlider', 'Number of parts :',10, 1, 32, None),
            ('downSlider', 'Download Speed :', 2**20 * 10, 2**10 * 8, 2**20 * 10, self.__byte_log),
            ('upSlider', 'Upload Speed :', 2**10, 2**10, 2**20 * 10, self.__byte_log),
        ]

        for name, title, value, _min, _max, f in sliders:
            wid = Slider(title, value, _min, _max, f)
            
            self.mainLayout.addWidget(wid)
            setattr(self, name, wid)


    def __byte_log(self, value):
        txt = 'MAX'
        if value < 10 * (2 ** 20):
            txt = sizeChanger(value)

        return txt


