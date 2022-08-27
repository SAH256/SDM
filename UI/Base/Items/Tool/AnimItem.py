from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from UI.Base.Label.AnimLabel import AnimLabel


# Animation Item for playing gif



class AnimItem(QtWidgets.QWidget):

    triggered = QtCore.pyqtSignal()

    def __init__(self, file_name):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self._anim(file_name)
    

    def _anim(self, file_name):
        self.animation = AnimLabel(file_name, loading = True)

        self.mainLayout.addWidget(self.animation)
    

    def mouseReleaseEvent(self, ev):
        super().mouseReleaseEvent(ev)

        self.triggered.emit()
    

    def enterEvent(self, ev):
        super().enterEvent(ev)

        self.animation.start()
    
    def leaveEvent(self, ev):
        super().leaveEvent(ev)

        self.animation.stop()





