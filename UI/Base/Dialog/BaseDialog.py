from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


# Base Dialog class for all UI dialogs


class Dialog(QDialog):

    def __init__(self, parent, icon_name = None):
        super().__init__(parent)

        flags = self.windowFlags()
        flags ^= Qt.WindowType.WindowContextHelpButtonHint
        flags |= Qt.WindowType.WindowCloseButtonHint

        self.setWindowFlags(flags)

        if icon_name:
            self.setWindowIcon(QIcon(icon_name))




