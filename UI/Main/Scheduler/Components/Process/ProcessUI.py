
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from Utility.Core import QUEUE
from Utility.Actions import check_os

from .Post.PostControl import PostProcess
from .Sub.SubControl import SubProcess


# Process section of Scheduler
class Process(QtWidgets.QScrollArea):

    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAutoFillBackground(True)

        wid = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QVBoxLayout()
        wid.setLayout(self.mainLayout)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        self.setWidget(wid)
        self.setWidgetResizable(True)

        self._process()
        self.mainLayout.addStretch()

        self.data = None

        name = 'area'
        self.setObjectName(name)

        name = 'widget'
        wid.setObjectName(name)

        self.__apply_style()


    def _process(self):
        items = [
            ('sub', SubProcess),
            ('post', PostProcess),
        ]

        for item in items:
            wid = item[1]()

            self.mainLayout.addWidget(wid)
            setattr(self, item[0], wid)


    def set_data(self, data):
        self.data = data
        self.__setup()


    def __setup(self):
        if self.data:
            self.sub.set_data(self.data.sub_process)
            self.post.set_data(self.data.post_process)


    def apply(self):
        if self.data:

            temp_sub = self.sub.get_data()
            temp_post = self.post.get_data()

            p = QUEUE.PROCESS.POST
            opt = temp_post.get(p.TURN_OFF)

            result = check_os(opt)

            if result:

                self.data.sub_process = temp_sub
                self.data.post_process = temp_post


    def __apply_style(self):
        style = '''
        #area {
            border : none;
            background-color : transparent;
        }

        #widget {
            background-color : transparent;
        }
        '''

        self.setStyleSheet(style)

