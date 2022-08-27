
from PyQt5 import QtWidgets

from UI.Base.CheckBox.StyledCheckBox import CheckBox
from UI.Base.Button.StyledButton import StyleButton
from UI.Base.Input.StyledInput import StyleInput

from Utility.Core import QUEUE

from ..Base import Base


# Widget for controlling sub-process of a queue - UI class
class SubUI(Base):

    def __init__(self):
        super().__init__()

        txt = 'Sub-process'
        self.set_title(txt)

        self.widgets = {}

        self._checks()
        self.__input()

        self._add_shadow()


    def _checks(self):
        s = QUEUE.PROCESS.SUB

        checks = [
            (s.MOVE_DIR, 'Move completed task to this dir'),
            (s.MOVE_END, 'Move failed task to the end of queue'),
            (s.BEEP, 'play BEEP when a task done'),
        ]

        for item in checks:
            wid = CheckBox(item[1], False)

            self.widgets[item[0]] = wid
            self.conLayout.addWidget(wid)


    def __input(self):
        ind = 1
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 3, 0, 5)
        self.conLayout.insertLayout(ind, layout)

        self.dirInput = StyleInput()
        self.dirInput.setReadOnly(True)

        self.browseBtn = StyleButton('', 'Browse')
        self.browseBtn.setEnabled(False)

        layout.addWidget(self.dirInput, 10)
        layout.addWidget(self.browseBtn, 1)

