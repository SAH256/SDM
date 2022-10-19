from PyQt5.QtCore import Qt

from .ToolItem import ToolItem

# Tool item Control class



class ToolItemControl(ToolItem) :

    def __init__(self, parent, icon_name, action):
        super().__init__(parent, icon_name)

        self.action = action
        self.setToolTip(self.action.toolTip())

        self.entered = False

        self._toggle_icon()



    def mousePressEvent(self, ev):
        super().mousePressEvent(ev)

        if ev.button() == Qt.MouseButton.LeftButton:
            self.action.triggered.emit()
    
    def _refresh(self):
        self._toggle_icon()
