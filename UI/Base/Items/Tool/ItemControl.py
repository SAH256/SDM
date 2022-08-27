from PyQt5.QtCore import Qt

from .ToolItem import ToolItem

# Tool item Control class



class ToolItemControl(ToolItem) :

    def __init__(self, icon_name, action):
        super().__init__(icon_name)

        self.action = action
        self.setToolTip(self.action.toolTip())

        name = 'action'
        self.setObjectName(name)

        self.entered = False

        self._toggle_icon()
        self.__apply_style()



    def mousePressEvent(self, ev):
        super().mousePressEvent(ev)

        if ev.button() == Qt.MouseButton.LeftButton:
            self.action.triggered.emit()


    def __apply_style(self):
        style = '''

        #action {
            background-color : transparent;
        }

        QToolTip {
            background-color : #444;
            color : #fff;
            padding : 3px 5px;
            border-radius : 3px;
            border : 1px solid #222;
            opacity : 200;
        }
        '''

        self.setStyleSheet(style)


