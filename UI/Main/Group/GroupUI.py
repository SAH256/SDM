
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from UI.Base.Dialog.BaseDialog import Dialog
from UI.Base.CheckBox.StyledCheckBox import CheckBox
from UI.Base.Input.StyledInput import StyleInput
from UI.Base.Button.StyledButton import StyleButton

from UI.Main.List.GroupList import View
from UI.Main.Boxes.SliderPane.PaneControl import PaneControl

from Utility.Core import ICONS, SELECTORS
from Utility.Gui import get_icon

from .Component.Save.SaveControl import SaveControl


# Group dialog -- UI class
class GroupUI(Dialog):

    def __init__(self, parent):
        super().__init__(parent, ICONS.DIALOGS.GROUP)

        self.setWindowModality(Qt.WindowModality.WindowModal)

        w, h = 900, 650
        title = "Group Download"

        self.resize(w, h)
        self.setWindowTitle(title)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self._header()
        self._list()
        self._footer()

        self.mainLayout.addStretch()

        name = 'group-dialog'
        self.setObjectName(name)


    def _header(self):
        self.headerLayout = QtWidgets.QHBoxLayout()
        self.headerLayout.setContentsMargins(0, 10, 0, 20)
        self.mainLayout.addLayout(self.headerLayout)

        self.__label()
        self.__icon()
        self.headerLayout.addStretch(1)
        self.__checks()


    def __label(self):
        layout = QtWidgets.QHBoxLayout()
        self.headerLayout.addLayout(layout)

        text = 'Group Download'
        name = 'dialog-header'

        label = QtWidgets.QLabel(text)
        label.setObjectName(name)

        layout.addWidget(label)


    def __icon(self):
        layout = QtWidgets.QHBoxLayout()
        self.headerLayout.addLayout(layout)

        text = 'Click items to select for adding to SDM list'
        icon_name = ICONS.OTHER.INFO
        size = 12

        label = QtWidgets.QLabel()
        label.setPixmap(get_icon(icon_name).pixmap(size, size))
        label.setToolTip(text)

        layout.addWidget(label)


    def __checks(self):
        checkLayout = QtWidgets.QHBoxLayout()
        checkLayout.setContentsMargins(5, 0, 10, 0)
        self.headerLayout.addLayout(checkLayout)

        checks = [
            ('allCheck', 'Select All')
        ]

        for item in checks:
            if item:
                wid = CheckBox(item[1], False)

                checkLayout.addWidget(wid)
                setattr(self, item[0], wid)


    def _list(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 5, 0, 10)        
        self.mainLayout.addLayout(layout)

        self.itemList = View()
        
        layout.addWidget(self.itemList)

        self.mainLayout.setStretchFactor(layout, 10)


    def _footer(self):
        self.footerLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.footerLayout)

        self.__save_path()
        self.__sliders()
        self.__controls()


    def __save_path(self):
        saveLayout = QtWidgets.QVBoxLayout()
        self.footerLayout.addLayout(saveLayout)

        self.saveBox = SaveControl()

        saveLayout.addWidget(self.saveBox)


    def __sliders(self):
        sliderLayout = QtWidgets.QVBoxLayout()
        sliderLayout.setContentsMargins(10, 0, 10, 0)
        self.footerLayout.addLayout(sliderLayout)

        self.sliderPane = PaneControl()

        sliderLayout.addWidget(self.sliderPane)


    def __controls(self):
        self.conLayout = QtWidgets.QVBoxLayout()
        self.footerLayout.addLayout(self.conLayout)

        self.__inputs()
        self.conLayout.addStretch(1)
        self.__buttons()
    

    def __inputs(self):
        inputLayout = QtWidgets.QVBoxLayout()
        self.conLayout.addLayout(inputLayout)

        text = 'Replace file name using asterisk(*) pattern:'
        label = QtWidgets.QLabel(text)
        label.setContentsMargins(0, 0, 0, 5)
        inputLayout.addWidget(label)

        inputs = [
            ('nameBox', False)
        ]

        for item in inputs:
            if item:
                wid = StyleInput()

                inputLayout.addWidget(wid)
                setattr(self, item[0], wid)
    

    def __buttons(self):
        btnLayout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(btnLayout)

        self.sizeBox = QtWidgets.QLabel('0 B')
        btnLayout.addWidget(self.sizeBox)

        btnLayout.addStretch(1)

        btns = [
            ('addBtn', 'ADD', SELECTORS.STATES.CONFIRM),
            ('cancelBtn', 'CANCEL', None),
        ]

        for item in btns:
            if item:
                wid = StyleButton(None, item[1])

                if item[2]:
                    wid.set_type(item[2])

                btnLayout.addWidget(wid)
                setattr(self, item[0], wid)
