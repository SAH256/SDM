
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class StyleScrollBar(QtWidgets.QScrollBar):

    def __init__(self, orientation):
        super().__init__(orientation)

        margins = (5, 4, 5, 4)
        
        if orientation == Qt.Orientation.Vertical:
            margins = margins[::-1]

        self.setContentsMargins(*margins)

        self.__apply_style()
    

    def __apply_style(self):
        style = '''
            QScrollBar:horizontal {
                        
                height: 4px;
                padding : 4px 2px;
                margin: -20px 0px -10px 0px;
                border-radius : 2px;
            }

            QScrollBar:vertical {
                width : 4px;
                padding : 2px 4px;
                border-radius : 2px;
                margin : 5px -5px 5px -5px;
            }

            QScrollBar::handle {
                background-color: #aaa;
            }

            QScrollBar::handle:horizontal {
                min-width: 200px;            
            }

            QScrollBar::handle:vertical {
                min-height : 150px;
                padding : 5px;
            }

            QScrollBar::handle:horizontal:hover,
            QScrollBar::handle:vertical:hover {
                background-color : #bbb;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::add-line:vertical {
                background-color : white;
            }

            QScrollBar::sub-line:horizontal,
            QScrollBar::sub-line:vertical {
                background-color : white;
            }
        '''

        self.setStyleSheet(style)






