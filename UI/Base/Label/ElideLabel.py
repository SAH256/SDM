from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt


# Label for minimizing text with ... notation



class Elide(QtWidgets.QLabel):

    _elideMode = Qt.TextElideMode.ElideMiddle

    def __init__(self, parent, per = 0.6):
        super().__init__(parent)

        self.percentage = per

        p = self.sizePolicy()
        p.setHorizontalPolicy(p.Policy.Minimum)
        # p.setVerticalPolicy()
        self.setSizePolicy(p)

        self.__apply_style()
    
    def elideMode(self):
        return self._elideMode
    
    def setElideMode(self, mode):
        if self._elideMode != mode and mode != Qt.TextElideMode.ElideNone:
            self._elideMode = mode
            self.update()
    
    def __apply_style(self):
        style = '''
        QLabel {
            padding-right : 50px;
        }
        '''

        self.setStyleSheet(style)

    def paintEvent(self, ev):

        p = QtGui.QPainter(self)

        pt = self.parentWidget()
        fm = self.fontMetrics()
        w = 100

        if pt:
            w = pt.width() * self.percentage
            w = int(w)


        self.setMaximumWidth(w)
        elide = fm.elidedText(self.text(), self.elideMode(), w - self.margin())

        p.drawText(self.rect(), self.alignment(), elide)












