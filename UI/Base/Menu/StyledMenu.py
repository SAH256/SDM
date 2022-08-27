
from PyQt5 import QtWidgets, QtCore



class StyleMenu(QtWidgets.QMenu):

    def __init__(self, title = ''):
        super().__init__(title)

        self.__apply_style()        


    def __apply_style(self):
        MENU_STYLE = '''

        QMenu {
            background-color: #303030;
            margin : 0px;
            padding : 0px;
        }

        QMenu::item {
            margin : 2px 0px;
            padding: 4px 40px 4px 10px;
            color : #eee;
            font-size : 14px;
        }

        QMenu::item:disabled {
            color : #888;
        }

        QMenu::item:enabled:selected {
            background-color: #505050;
        }

        QMenu::item:enabled:pressed {
            padding-left : 15px;
        }

        QMenu::separator {
            height: 1px;
            background: #ccc;
            margin : 0xp 7px;
        }

        '''

        self.setStyleSheet(MENU_STYLE)















