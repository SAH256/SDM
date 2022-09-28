
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from UI.Base.Dialog.BaseDialog import Dialog
from UI.Base.Button.StyledButton import StyleButton

from UI.Main.Tab.Option.InfiniteControl import InfiniteControl

from Utility.Core import ICONS

from .Components.List.ListControl import List
from .Components.Timer.TimerControl import TimerControl
from .Components.File.FileControl import File
from .Components.Process.ProcessUI import Process
from .Components.Setting.SettingControl import Setting



# Scheduler diaog for managing queues -- UI class
class SchedulerUI(Dialog):

    def __init__(self, parent):
        super().__init__(parent, ICONS.DIALOGS.TIMER)

        title = 'Task Scheduler'
        self.setWindowTitle(title)

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.mainLayout.setContentsMargins(5, 5, 5, 10)

        w, h = 850, 600
        self.resize(w, h)

        self._list()
        self._content()
        self.__add_tabs()

        name = 'panel'
        self.setObjectName(name)

        # self.__apply_style()


    def _list(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 20, 0)
        self.mainLayout.addLayout(layout, 2)

        self.queueList = List()

        layout.addWidget(self.queueList)


    def _content(self):
        self.conLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.conLayout, 6)
        self.mainLayout.setStretchFactor(self.conLayout, 6)

        self.__tab()
        self.__stack()
        self.__buttons()


    def __stack(self):
        layout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(layout)

        self.conLayout.setAlignment(layout, Qt.AlignmentFlag.AlignCenter)

        self.stackLayout = QtWidgets.QStackedLayout()

        layout.addLayout(self.stackLayout)

        layout.setAlignment(self.stackLayout, Qt.AlignmentFlag.AlignCenter)


    def __tab(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 20)
        self.conLayout.addLayout(layout)

        _dir = QtWidgets.QBoxLayout.Direction

        self.tab = InfiniteControl(self, _dir.LeftToRight, False)

        layout.addWidget(self.tab, 1, Qt.AlignmentFlag.AlignCenter)


    def __buttons(self):
        layout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(layout)

        buttons = [
            ('startBtn', 'Start', True),
            None,
            ('helpBtn', 'Help', True),
            None,
            ('applyBtn', 'Apply', False),
            ('closeBtn', 'Close', True),
        ]

        for item in buttons:
            if item:
                wid = StyleButton('', item[1])

                layout.addWidget(wid)
                setattr(self, item[0], wid)
            else:
                layout.addStretch()


    def __add_tabs(self):

        widgets = {
            'timerOption'   : ('TIMER_INDEX',   ICONS.SCHEDULER.TIMING,  'Time setting',      TimerControl),
            'fileOption'    : ('FILE_INDEX',    ICONS.SCHEDULER.FILE,    'Files in the queue', File),
            'processOption' : ('PROCESS_INDEX', ICONS.SCHEDULER.PROCESS, 'Process',           Process),
            'settingOption' : ('SETTING_INDEX', ICONS.SCHEDULER.SETTING, 'Setting',           Setting),
        }

        for name, item in widgets.items():
                
            wid = item[3]()
            index = self.stackLayout.addWidget(wid)

            self.tab.add_item(item[1], item[2])

            setattr(self, item[0], index)
            setattr(self, name, wid)


    def __apply_style(self):
        style = '''
        #panel {
            background-color : white;
        }
        '''

        self.setStyleSheet(style)





