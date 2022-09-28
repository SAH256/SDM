
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


# Base widget for containing process sub sections
class Base(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self._title()
        self._content()

        name = 'panel'
        self.setObjectName(name)

        # self.__apply_style()


    def _add_shadow(self):
        e = QtWidgets.QGraphicsDropShadowEffect()
        e.setColor(Qt.GlobalColor.gray)
        e.setOffset(0, 0)
        e.setBlurRadius(10)

        self.setGraphicsEffect(e)


    def _title(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 5, 0, 10)
        self.mainLayout.addLayout(layout)

        self.title = QtWidgets.QLabel()
        layout.addWidget(self.title)

        name = 'title'
        self.title.setObjectName(name)


    def _content(self):
        self.conLayout = QtWidgets.QVBoxLayout()
        self.conLayout.setContentsMargins(10, 0, 0, 5)
        self.mainLayout.addLayout(self.conLayout)


    def set_title(self, txt):
        if txt and isinstance(txt, str):
            self.title.setText(txt)


    def __apply_style(self):
        style = '''
        #panel {
            background-color : white;
        }

        #title {
            font-family : Arial;
            font-size : 16px;
            font-weight : 600;
            color : darkcyan;
        }

        #danger {
            color : red;
            font-size : 14px;
            font-weight : 600;
            text-align : center;
        }
        '''

        self.setStyleSheet(style)

