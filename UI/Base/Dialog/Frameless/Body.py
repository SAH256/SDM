from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt




class Body(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        name = 'popup-body'
        self.setObjectName(name)


