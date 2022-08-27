from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt




class Body(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        name = 'body'
        self.setObjectName(name)
        
        self.__apply_style()
    
    
    def __apply_style(self):
        style = '''
        #body {
            background-color : white;
            border-bottom-right-radius : 4px;
            border-bottom-left-radius : 4px;
        }
        
        '''
        
        self.setStyleSheet(style)
















