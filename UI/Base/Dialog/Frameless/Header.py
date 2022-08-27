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
        
        name = 'header'
        self.setObjectName(name)

        self.__apply_style()


    def _title(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)
        
        name = 'title'
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





    def __apply_style(self):
        style = '''
        #header {
            background-color : #3b3b3b;
            border-top-left-radius : 4px;
            border-top-right-radius : 4px;
        }
        
        #header[css-class = "confirm"] {
            background-color : #4096ff;
        }
        
        #header[css-class = "info"] {
            background-color : #53ff30;
        }
        
        #header[css-class = "warning"] {
            background-color : #d8d800;
        }
        
        #header[css-class = "danger"] {
            background-color : #ff3433;
            /* background-color : #fd0046; */
        }
        
        #title {
            font-family : Arial;
            font-size : 16px;
            /* font-weight : 600; */
            color : white;
        }

        
        '''
        
        self.setStyleSheet(style)
   






















