from PyQt5 import QtWidgets

from UI.Base.ComboBox.StyledComboBox import ComboBox


# Category selector mini widget -- UI class
class CategoryUI(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)
        
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self._label()
        self._combo()


    def _label(self):
        labelLayout = QtWidgets.QHBoxLayout()
        labelLayout.setContentsMargins(0, 0, 5, 0)
        self.mainLayout.addLayout(labelLayout)

        text = 'Category'
        label = QtWidgets.QLabel(text)

        labelLayout.addWidget(label)


    def _combo(self):
        comboLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(comboLayout, 10)

        self.category = ComboBox()

        comboLayout.addWidget(self.category)

