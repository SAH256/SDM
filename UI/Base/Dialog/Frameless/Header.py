from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, pyqtSignal

from UI.Base.Button.StyledButton import StyleButton

from Utility.Core import ICONS


# Header/TitleBar of frameless dialog




class Header(QtWidgets.QWidget):

    close_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.mainLayout)
        
        h = 40
        self.setFixedHeight(h)
        
        self._title()
        self.mainLayout.addStretch()
        self._btn()
        
        self.prop_name = 'css-class'
        
        name = 'popup-header'
        self.setObjectName(name)


    def _title(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)
        
        name = 'popup-header__title'
        self.title = QtWidgets.QLabel()
        self.title.setObjectName(name)
        
        layout.addWidget(self.title)
    
    
    def _btn(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)
        
        
        names = [
            # 'Icons/minimize.png',
            # 'Icons/maximize.png',
            ('closeBtn', ICONS.OTHER.CLOSE_WHITE),
        ]
        
        size = 12
        
        for item in names:

            wid = QtWidgets.QLabel()
            wid.setContentsMargins(5, 0, 0, 0)
            wid.setPixmap(QtGui.QIcon(item[1]).pixmap(size, size))
        
            layout.addWidget(wid)
            setattr(self, item[0], wid)




    def set_title(self, text):
        self.title.setText(text)



    def set_state(self, state):
        self.setProperty(self.prop_name, state)
        self.update()



    def update(self):
        self.style().unpolish(self)
        self.style().polish(self)
        
        super().update()


    def mouseReleaseEvent(self, ev):
        super().mouseReleaseEvent(ev)

        child = self.childAt(ev.pos())

        if child == self.closeBtn:
            self.close_requested.emit()


