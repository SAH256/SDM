
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from UI.Base.Label.AnimLabel import AnimLabel
from UI.Base.Input.StyledInput import StyleInput
from UI.Base.Input.StyleTextArea import TextArea
from UI.Base.CheckBox.StyledCheckBox import CheckBox
from UI.Base.Button.StyledButton import StyleButton
from UI.Base.Dialog.BaseDialog import Dialog

from UI.Main.Boxes.Torrent.TorrentControl import TorrentControl
from UI.Main.Boxes.Save.SaveControl import SaveControl
from UI.Main.Boxes.Category.CategoryControl import CategoryControl
from UI.Main.Boxes.Auth.AuthControl import AuthControl
from UI.Main.Boxes.SliderPane.PaneControl import PaneControl

from Utility.Core import CATEGORY, ICONS, SELECTORS


# Add URL dialog -- UI class
class AddUI(Dialog):

    def __init__(self, parent):
        super().__init__(parent, ICONS.DIALOGS.ADD)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        w, h = 500, 400
        max_size = 550
        title = 'Add New File'
        
        self.resize(w, h)
        self.setMaximumSize(max_size, max_size)
        self.setWindowTitle(title)

        self.widgets = []
        
        self._header()
        self._contents()
        self.mainLayout.addStretch(1)
        self._btn()

        name = 'add'
        self.setObjectName(name)

        # self.__apply_style()


    def _header(self):
        self.headLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.headLayout)

        self.__task_name()
        self.headLayout.addStretch()
        self.__loading()


    def __task_name(self):
        layout = QtWidgets.QHBoxLayout()
        self.headLayout.addLayout(layout)

        name = 'header'

        labels = [
            (None, 'Download'),
            ('name_header', 'File'),
            None
        ]

        for item in labels:
            if item:
                wid = QtWidgets.QLabel(item[1], self)
                wid.setObjectName(name)
                
                layout.addWidget(wid)

                if item[0]:
                    setattr(self, item[0], wid)
            else:
                layout.addStretch()



    def __loading(self):
        layout = QtWidgets.QHBoxLayout()
        self.headLayout.addLayout(layout)

        path = ICONS.ANIMATION.RHOMBUS
        size = 25
        is_loading = True

        self.loading = AnimLabel(path, size, is_loading)
        self.loading.setVisible(False)

        layout.addWidget(self.loading)
        

    def _contents(self):
        self.conLayout = QtWidgets.QVBoxLayout()
        self.conLayout.setSpacing(8)
        self.mainLayout.addLayout(self.conLayout)
        
        self.__error()
        self.__url()
        self.__name()
        self.__size()
        self.__torrent()
        self.__save()
        self.__checks()
        self.__category()
        self.__twins()

    
    def __error(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 5, 0, 5)
        self.conLayout.addLayout(layout)

        name = 'warning'
        self.error_label = QtWidgets.QLabel(name)
        self.error_label.setVisible(False)
        self.error_label.setObjectName(name)

        layout.addWidget(self.error_label)


    def __url(self):
        layout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(layout)

        place = 'Enter URL here...'
        self.link_input = TextArea()
        self.link_input.setPlaceholderText(place)

        layout.addWidget(self.link_input)


    def __name(self):
        layout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(layout)

        inputs = [
            ('file_name', 'File Name', 9, TextArea),
            ('extension', 'Extension', 2, StyleInput),
        ]

        for item in inputs:
            wid = item[-1]()
            wid.setPlaceholderText(item[1])

            layout.addWidget(wid, item[2])
            layout.setAlignment(wid, Qt.AlignmentFlag.AlignBottom)

            self.widgets.append(wid)
            setattr(self, item[0], wid)


    def __size(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 10)
        self.conLayout.addLayout(layout)

        labels = [
            (None, 'Size : ', 'size'),
            ('size_label', '', 'size'),
            None
        ]

        for item in labels:
            if item:
                wid = QtWidgets.QLabel(item[1])
                wid.setObjectName(item[2])

                layout.addWidget(wid)

                if item[0]:
                    setattr(self, item[0], wid)
        
            else:
                layout.addStretch(1)


    def __torrent(self):
        layout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(layout)

        self.torrent_option = TorrentControl()
        self.torrent_option.setVisible(False)

        self.widgets.append(self.torrent_option)

        layout.addWidget(self.torrent_option)


    def __save(self):
        layout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(layout)

        self.save = SaveControl()
        self.widgets.append(self.save)

        layout.addWidget(self.save)


    def __checks(self):
        layout = QtWidgets.QGridLayout()
        self.conLayout.addLayout(layout)

        checks = [
            ('retryCheck', 'Retry'),
            ('proxyCheck', 'Proxy'),
            ('advanceCheck', 'Advanced'),
            ('hiddenCheck', 'Hidden'),
            ('seqCheck', 'Sequential Download'),
        ]

        r = 0
        c = 0
        max_col = 3

        for item in checks:
            wid = CheckBox(item[1], False)

            layout.addWidget(wid, r, c)
            setattr(self, item[0], wid)

            c += 1

            if c == max_col:
                r += 1
                c = 0


    def __category(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 10, 0, 10)
        self.conLayout.addLayout(layout)

        self.category = CategoryControl([x for x in CATEGORY.CATEGORIES if x])
        self.category.setVisible(False)

        self.widgets.append(self.category)

        layout.addWidget(self.category)


    def __twins(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 10, 0, 10)
        self.conLayout.addLayout(layout)

        items = [
            ('sliders', PaneControl),
            ('auth', AuthControl),
        ]

        for item in items:
            wid = item[-1]()
            wid.setVisible(False)

            layout.addWidget(wid)
            self.widgets.append(wid)
            setattr(self, item[0], wid)

    
    def _btn(self):
        btnLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.LeftToRight)
        btnLayout.setContentsMargins(0, 10, 0, 0)
        self.mainLayout.addLayout(btnLayout)

        buttons = [
            ('cancelBtn', 'CANCEL', None),
            None,
            ('addBtn', 'ADD', SELECTORS.STATES.CONFIRM),
            ('startBtn', 'START', SELECTORS.STATES.CONFIRM),
        ]

        for btn in buttons:

            if btn:
                wid = StyleButton('', btn[1])

                if btn[2]:
                    wid.set_type(btn[2])

                btnLayout.addWidget(wid)
                setattr(self, btn[0], wid)
            
            else:
                btnLayout.addStretch(1)


    # def __apply_style(self):
    #     style = '''
    #     #add {
    #         background-color : white;
    #     }

    #     #header {
    #         font-family : Arial;
    #         font-size : 16px;
    #         font-weight : 600;
    #         color : blue;
    #     }

    #     #header[text="Torrent"] {
    #         color : red;
    #     }

    #     #size {
    #         font-size : 14px;
    #         color : blue;
    #     }


    #     #warning {
    #         font-family : Arial;
    #         font-size : 16px;
    #         font-weight : 600;
    #         color : red;
    #     }
    #     '''

    #     self.setStyleSheet(style)






