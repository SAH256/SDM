
from PyQt5 import QtWidgets

from UI.Base.CheckBox.StyledCheckBox import CheckBox
from UI.Base.Input.StyledInput import StyleInput
from UI.Base.Button.StyledButton import StyleButton
from UI.Base.ComboBox.StyledComboBox import ComboBox

from Utility.Core import QUEUE

from ..Base import Base


# Widget for controlling post-process of a queue - UI class
class PostUI(Base):
    
    def __init__(self):
        super().__init__()

        txt = 'Post-process'
        self.set_title(txt)

        self.widgets = {}

        self._checks()
        self.__input()
        self.__combo()

        self._label()

        self._add_shadow()


    def _checks(self):
        p = QUEUE.PROCESS.POST

        checks = [
            (p.OPEN_FILE, 'Open following when done', True),
            (p.EXIT_APP, 'Exit app when done', True),
            (p.TURN_OFF, 'Turn off computer when done', True),
            (p.FORCE_SHUT_DOWN, 'Force shutdown', False),
        ]

        for item in checks:
            layout = QtWidgets.QHBoxLayout()

            if not item[2]:
                layout.setContentsMargins(15, 0, 0, 0)

            wid = CheckBox(item[1], False)
            wid.setEnabled(item[2])

            self.widgets[item[0]] = wid

            layout.addWidget(wid)

            self.conLayout.addLayout(layout)


    def __input(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 10)

        self.dirInput = StyleInput()
        self.dirInput.setReadOnly(True)

        self.browseBtn = StyleButton('', 'Browse')
        self.browseBtn.setEnabled(False)

        layout.addWidget(self.dirInput, 10)
        layout.addWidget(self.browseBtn, 1)

        ind = 1
        self.conLayout.insertLayout(ind, layout)


    def __combo(self):
        layout = 3
        layout = self.conLayout.itemAt(layout)

        self.options = ComboBox()
        self.options.setEnabled(False)
        self.options.addItems(QUEUE.PROCESS.POST.OPTIONS)

        layout.addStretch(1)
        layout.addWidget(self.options)


    def _label(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 10, 0, 0)
        self.conLayout.addLayout(layout)

        msg = 'Need Administrator privilege'

        self.msgLabel = QtWidgets.QLabel(msg)
        self.msgLabel.setVisible(False)
        self.msgLabel.setObjectName('danger')

        layout.addWidget(self.msgLabel)



