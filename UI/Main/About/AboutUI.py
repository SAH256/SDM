from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize

from UI.Base.Dialog.BaseDialog import Dialog
from UI.Base.Button.StyledButton import StyleButton

from Utility.Core import ICONS


# About dialog UI
class AboutUI(Dialog):

    def __init__(self, parent):
        super().__init__(parent, ICONS.DIALOGS.ABOUT)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        w, h = 300, 400
        self.setFixedSize(w, h)

        self._image()
        self.mainLayout.addStretch(1)
        self._info()
        self._attributions()
        self._buttons()
        
        name = 'about-dialog'
        self.setObjectName(name)


    def _image(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)

        self.logo_place = QtWidgets.QLabel()
        layout.addWidget(self.logo_place, 1, Qt.AlignmentFlag.AlignCenter)


    def _info(self):
        self.infoLayout = QtWidgets.QFormLayout()
        self.infoLayout.setContentsMargins(10, 0, 10, 20)
        self.infoLayout.setHorizontalSpacing(50)
        self.mainLayout.addLayout(self.infoLayout, 0)


    def _attributions(self):
        title = 'Special thanks from'
        group = QtWidgets.QGroupBox()
        group.setTitle(title)

        self.mainLayout.addWidget(group)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        group.setLayout(layout)


        scroll = QtWidgets.QScrollArea()
        scroll.setFrameShape(scroll.Shape.NoFrame)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        name = 'attr-label'

        self.attr_box = QtWidgets.QLabel()
        self.attr_box.setObjectName(name)
        self.attr_box.setWordWrap(True)
        self.attr_box.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self.attr_box.setOpenExternalLinks(True)
        self.attr_box.setContentsMargins(5, 10, 0, 5)
        
        scroll.setWidget(self.attr_box)


    def _buttons(self):
        layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(layout)

        buttons = [
            ('githubBtn', ICONS.OTHER.GITHUB, None, 'Github'),
            None,
            ('okBtn', None, 'OK', None),
        ]
        
        for item in buttons:
            if item:
                btn = StyleButton(*item[1:-1])

                if item[-1]:
                    btn.setToolTip(item[-1])

                layout.addWidget(btn)
                setattr(self, item[0], btn)

            else:
                layout.addStretch()


    def update(self):
        self.style().unpolish(self)
        self.style().polish(self)
        super().update()


