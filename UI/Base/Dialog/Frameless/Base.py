
from PyQt5 import QtWidgets , QtGui
from PyQt5.QtCore import Qt

from .Header import Header
from .Body import Body

from ..BaseDialog import Dialog


# Frameless dialog class for fancy popup dialogs



class FrameLessUI(Dialog):
    
    def __init__(self, parent):
        super().__init__(parent)

        flags = self.windowFlags()
        flags ^= Qt.WindowType.WindowContextHelpButtonHint
        flags ^= Qt.WindowType.WindowCloseButtonHint
        flags |= Qt.WindowType.FramelessWindowHint

        self.setWindowFlags(flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        self.offset = None
        
        self._header()
        self._body()

        name = 'popup'
        self.setObjectName(name)

        self.__shadow()
        self.__apply_style()
    
    
    def _header(self):
        layout = QtWidgets.QVBoxLayout()
        self.layout().addLayout(layout)
        
        self.header = Header()
        self.header.close_requested.connect(self.close)
        
        layout.addWidget(self.header)


    def _body(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(1, 0, 1, 0)
        self.layout().setStretchFactor(layout, 4)
        self.layout().addLayout(layout)
        
        body = Body()
        layout.addWidget(body)
        
        self.mainLayout = body.layout()
        self.mainLayout.addStretch()



    def set_state(self, state):
        self.header.set_state(state)
    
    def set_title(self, title):
        self.header.set_title(title)



    def __shadow(self):
        e = QtWidgets.QGraphicsDropShadowEffect()
        e.setBlurRadius(10)
        e.setOffset(0, 0)
        e.setColor(QtGui.QColor(' #444'))
        self.setGraphicsEffect(e)



    def mousePressEvent(self, ev):
        child = self.childAt(ev.pos())
        
        if ev.button() == Qt.MouseButton.LeftButton and isinstance(child, Header):
            self.offset = ev.pos()
        else:
            super().mousePressEvent(ev)
            
        
        
    
    def mouseMoveEvent(self, ev):
        
        if self.offset:
            self.move(self.pos() + ev.pos() - self.offset)
        else:
            super().mouseMoveEvent(ev)


    def mouseReleaseEvent(self, ev):
        super().mouseReleaseEvent(ev)
        self.offset = None



    def __apply_style(self):
        style = '''
        #popup {
            background-color : transparent;
        }

        '''
        
        self.setStyleSheet(style)








