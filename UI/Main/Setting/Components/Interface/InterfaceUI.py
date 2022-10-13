
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt


from UI.Base.ComboBox.StyledComboBox import ComboBox


# Setting Interface section -- UI class
class InterfaceUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self._combo()
        self.mainLayout.addStretch()


    def _combo(self):
        layout = QtWidgets.QFormLayout()
        self.mainLayout.addLayout(layout)

        combos = [
            ('themeCombo', 'Theme'),
            ('iconCombo', 'Icon package'),
            ('langCombo', 'Language'),
        ]

        for item in combos:
            wid = ComboBox()

            layout.addRow(item[1], wid)
            setattr(self, item[0], wid)
