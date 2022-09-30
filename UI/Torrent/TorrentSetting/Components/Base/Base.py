from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from UI.Base.ScrollBar.ScrollBarUI import StyleScrollBar



class BaseWidget(QtWidgets.QWidget):

    def __init__(self, box = True, vertical = False):
        super().__init__()
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.__layout(box, vertical)

        name = 'torrent-base-widget'
        self.setObjectName(name)


    def __layout(self, box, vertical):
        layout = None

        if box:
            layout = QtWidgets.QGridLayout()
        else:
            if vertical:
                layout = QtWidgets.QVBoxLayout()
            else:
                layout = QtWidgets.QHBoxLayout()
        
        self.mainLayout = layout
        self.setLayout(self.mainLayout)



class BasePanel(BaseWidget):
    
    def __init__(self, box, vertical = False):
        super().__init__(box, vertical)

        self.info_data = None
        self.paused = True


    def set_data(self, data):
        self.info_data = data
    
    def set_paused(self, state):
        self.paused = state



class Scroll(QtWidgets.QScrollArea):

    def __init__(self):
        super().__init__()

        self.setFrameShape(self.Shape.NoFrame)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.setWidgetResizable(True)

        self.info_data = None
        self.paused = True

        name = 'torrent-scroll_area'
        self.setObjectName(name)

        self.__scroll_bar()


    def _widget(self, box, vertical):
        widget = BaseWidget(box, vertical)
        self.mainLayout = widget.layout()
        self.setWidget(widget)
    

    def __scroll_bar(self):

        sc = StyleScrollBar(Qt.Orientation.Vertical)
        self.setVerticalScrollBar(sc)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


    def enterEvent(self, ev):
        super().enterEvent(ev)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def leaveEvent(self, ev):
        super().enterEvent(ev)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)




def create_icon_label(icon_name, size = 15):
    
    temp = QtWidgets.QLabel()
    temp.setPixmap(QtGui.QIcon(icon_name).pixmap(size, size))

    return temp



