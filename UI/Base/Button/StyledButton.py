
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

# Base Button class for modifying its style and behaviour




class StyleButton(QtWidgets.QPushButton):
    
    def __init__(self, icon, text):
        super().__init__(text)

        if icon:
            self.setIcon(QtGui.QIcon(icon))

        self.prop_name = 'css-class'
        self.icon_prop = 'icon'

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.__apply_style()



    def set_type(self, _type):
        if _type:
            self.setProperty(self.prop_name, _type)

    # assigning style SELECTOR
    def set_selector(self, name):
        self.setObjectName(name)

    # change style to icon button style
    def icon_selector(self, state):
        name = ''

        if state:
            name = self.icon_prop
        
        if name:
            self.setProperty(self.prop_name, name)
            self.update()
    

    def update(self):
        self.style().unpolish(self)
        self.style().polish(self)
        super().update()
        
    def __apply_style(self):

        style = '''
                
        QPushButton {
            padding : 6px 10px;
            border-radius : 4px;
            border : 2px solid transparent;
            outline : none;
            background-color : #dbdbdb;
            color : #333;
            
            font-family : Arial;
            /* font-weight : 600; */
            font-size : 14px;
        }

        QPushButton:disabled {
            background-color : #c9c9c9;
            color : #555;
        }
        
        QPushButton:hover {
            background-color : #d2d2d2;
        }
        
        QPushButton:pressed {
            background-color : #ccc;
            color : #555;
        }

        QPushButton:menu-indicator {
            width : 10px;
            height : 100%;
            subcontrol-position : right center;
            subcontrol-origin : padding;
            
            image : url("assets/Icons/Default/Other/arrow_down_white.png");
            padding : 2px 5px 2px 0px;
        }

        /* 
        QPushButton:menu-indicator:hover {
            border-color : transparent;
        }
        */



        QPushButton[css-class = "confirm"] {
            background-color : #4056ff;
            color : white;
        }

        QPushButton[css-class = "confirm"]:disabled {
            background-color : #2d53b5;
        }
        
        QPushButton[css-class = "confirm"]:pressed {
            background-color : #4076ff;
            color : #ddd;
        }

        
        
        QPushButton[css-class = "danger"] {
            background-color : #ff3233;
            color : white;
        }


        QPushButton[css-class = "danger"]:disabled {
            background-color : #c42929;

        }
        
        QPushButton[css-class = "danger"]:pressed {
            background-color : #ee3535;
            color : #ddd;
        }
        
        
        QPushButton[css-class = "warning"] {
            background-color : #d8d800;
            color : white;
        }


        QPushButton[css-class = "warning"]:disabled {
            background-color : #c8b800;

        }
        
        QPushButton[css-class = "warning"]:pressed {
            background-color : #d8c800;
            color : #ddd;
        }

        QPushButton[css-class = "icon"] {
            padding : 10px;
            border-radius : 12px;
            background-color : transparent;
        }
        
        QPushButton[css-class = "icon"]:hover {
            background-color : #ddd;
        }

        '''

        self.setStyleSheet(style)




















