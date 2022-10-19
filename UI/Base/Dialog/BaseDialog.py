from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from Utility.Gui import get_icon

# Base Dialog class for all UI dialogs


class Dialog(QDialog):

    def __init__(self, parent, icon_name = None):
        super().__init__(parent)

        flags = self.windowFlags()
        flags ^= Qt.WindowType.WindowContextHelpButtonHint
        flags |= Qt.WindowType.WindowCloseButtonHint

        self.setWindowFlags(flags)

        if icon_name:
            self.setWindowIcon(get_icon(icon_name))




