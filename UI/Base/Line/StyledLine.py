
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class Line(QtWidgets.QWidget):
    
    def __init__(self, width = 1, color = 'black', horizontal = True):
        super().__init__()

        self._width = width
        self._color = color


        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # self.setContentsMargins(0, 50, 0, 0)


        css_attr = 'orientation'
        value = 'v'
        w, h = 3, 30

        if horizontal:
            value = 'h'
            t = w
            h = w
            w = t
            
        self.setFixedSize(w, h)
        self.setProperty(css_attr, value)


        name = 'line'
        self.setObjectName(name)

        self.__apply_style()



        
    def __apply_style(self):
        style = f'''
        #line {{
            border-color : {self._color};
            border-style : solid;
            border-radius : 1px;
        }}

        #line[orientation="h"] {{
            border-bottom-width : {self._width}px;
        }}

        #line[orientation="v"] {{
            border-left-width : {self._width}px;
        }}
        '''

        self.setStyleSheet(style)











