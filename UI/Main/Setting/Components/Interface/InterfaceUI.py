
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

        self.data = None

    

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
    



    def set_data(self, data):
        self.interface_data = data

        self.__setup()


    def __setup(self):
        self.iconCombo.addItems(self.interface_data.asset_pack_names())
        self.iconCombo.setCurrentText(self.interface_data.current_icon_pack())

        self.themeCombo.addItems(self.interface_data.theme_names())
        self.themeCombo.setCurrentText(self.interface_data.current_theme())

        self.langCombo.addItems(self.interface_data.lang_names())
        self.langCombo.setCurrentText(self.interface_data.current_lang())




