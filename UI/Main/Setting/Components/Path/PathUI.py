from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from UI.Base.ComboBox.StyledComboBox import ComboBox
from UI.Base.Button.StyledButton import StyleButton
from UI.Base.Input.StyledInput import StyleInput
from UI.Base.Input.StyleTextArea import TextArea

from Utility.Core import ICONS


# Setting Path section -- UI class
class PathUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self._top()
        self.mainLayout.addStretch(1)
        
        self._center()

        self._bottom()
        self.mainLayout.addStretch(2)



    def _top(self):
        layout = QtWidgets.QFormLayout()
        self.mainLayout.addLayout(layout)

        text = 'Category'
        
        self.categoryCombo = ComboBox()
        
        layout.addRow(text, self.categoryCombo)


    def _center(self):
        self.centerLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.centerLayout)
        text = 'Category Save Path :'

        self.__label(self.centerLayout, text)
        self.__path_select()


    def __label(self, parent_layout, text):
        layout = QtWidgets.QHBoxLayout()
        parent_layout.addLayout(layout)

        label = QtWidgets.QLabel(text)

        layout.addWidget(label)


    def __path_select(self):
        self.pathLayout = QtWidgets.QHBoxLayout()
        self.centerLayout.addLayout(self.pathLayout)

        self.__input()
        self.__btn()
    

    def __input(self):
        layout = QtWidgets.QHBoxLayout()
        self.pathLayout.addLayout(layout)

        self.pathInput = StyleInput()

        layout.addWidget(self.pathInput)
    
    def __btn(self):
        layout = QtWidgets.QHBoxLayout()
        self.pathLayout.addLayout(layout)

        self.browseBtn = StyleButton(ICONS.OTHER.BROWSE_1, '')

        layout.addWidget(self.browseBtn)
    

    def _bottom(self):
        self.bottomLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.bottomLayout)

        text = 'Supported Extension :'

        self.__label(self.bottomLayout, text)
        self.__textarea()



    def __textarea(self):

        layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(layout)

        self.extension = TextArea()

        layout.addWidget(self.extension)






