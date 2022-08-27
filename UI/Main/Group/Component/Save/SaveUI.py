
from PyQt5 import QtWidgets

from UI.Base.ComboBox.StyledComboBox import ComboBox
from UI.Main.Boxes.Save.SaveControl import SaveControl
from UI.Main.Boxes.Category.CategoryControl import CategoryControl

from Utility.Core import CATEGORY


# Group dialog, Save section -- UI class
class SaveUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self._options()
        self._stacks()


    def _options(self):
        optionLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(optionLayout)

        text = 'Save Based on : '
        label = QtWidgets.QLabel(text)

        items = [
            'Task Default',
            'One Category',
            'One Directory'
        ]

        self.optionBox = ComboBox()
        self.optionBox.addItems(items)
        
        optionLayout.addWidget(label)
        optionLayout.addWidget(self.optionBox, 2)


    def _stacks(self):
        self.stackLayout = QtWidgets.QStackedLayout()
        self.stackLayout.setContentsMargins(0, 10, 0, 0)
        self.mainLayout.addLayout(self.stackLayout)

        self.__default_option()
        self.__category_option()
        self.__directory_option()


    def __default_option(self):
        wid = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        wid.setLayout(layout)

        self.DEFAULT_INDEX = self.stackLayout.addWidget(wid)


    def __category_option(self):
        self.category = CategoryControl([x for x in CATEGORY.CATEGORIES if x])
        self.CATEGORY_INDEX = self.stackLayout.addWidget(self.category)


    def __directory_option(self):
        self.pathBox = SaveControl()
        self.pathBox.set_path('C:\\')

        self.DIRECTORY_INDEX = self.stackLayout.addWidget(self.pathBox)

