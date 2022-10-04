from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import pyqtSignal

from UI.Base.Items.Tool.ItemControl import ToolItemControl
from UI.Base.Items.Tool.AnimItem import AnimItem


from Utility.Core import CATEGORY, ACTIONS, FILTER, STATES, LINK_TYPE

from .mainUI import MainUI


# Main window central widget -- UI class
class UIControl(MainUI):

    requested = pyqtSignal(str, int)

    def __init__(self, parent):
        super().__init__(parent)
        self.__connect_slots()


    def __connect_slots(self):
        self.taskList.selection_changed.connect(self.__task_state_handler)
        self.taskList.menu_requested.connect(self.__task_menu_handler)
        self.categoryTab.item_changed.connect(self.__cat_handler)
        self.headerTab.item_changed.connect(self.__cat_handler)


    def __cat_handler(self, info):
        _type = info[0]
        data = info[1]

        if _type == FILTER.CATEGORY:
            self.taskList.set_category(data)

        elif _type == FILTER.STATUS:
            self.taskList.set_state(data[0])
            self.taskList.set_status(data[1])
            self.taskList.set_queue(None)

        elif _type == FILTER.QUEUE:
            self.taskList.set_state(None)
            self.taskList.set_status(None)
            self.taskList.set_queue(data)
        else:
            print(info)


    def add_categories(self, items):

        for item in items:

            icon = item[0]
            name = item[1]
            data = name

            if len(item) == 3:
                data = item[2]

            self.categoryTab.add_item(icon, name, FILTER.CATEGORY, data)


    def add_left_tools(self, items):

        for file_name, tip, handler in items:
            item = AnimItem(self, file_name)
            item.triggered.connect(handler)
            item.setToolTip(tip)
            self.toolTab.add_item(item)


    def add_headers(self, items):
        for icon, name, _type, data in items:
            self.headerTab.add_item(icon, name, _type, data)


    def add_actions(self, actions):

        for [name, enable], [icon, action] in actions.items():
            item = ToolItemControl(self.actionTab, icon, action)
            item.setEnabled(enable)
            self.actionTab.add_item(item)

            setattr(self, name, item)


    def get_selected(self):
        return self.taskList.get_selected()


    def __task_state_handler(self, states):

        run = [s not in [STATES.PAUSED, STATES.COMPLETED] for s in states]
        p = [s == STATES.PAUSED for s in states]

        self.resumeBtn.setEnabled(bool(p) and all(p))
        self.pauseBtn.setEnabled(bool(run) and all(run))
        self.removeBtn.setEnabled(bool(states))


    def _toggle_action_btn(self):

        r = True
        p = False

        if self.resumeBtn.isEnabled():
            r = False
            p = True

        self.resumeBtn.setEnabled(r)
        self.pauseBtn.setEnabled(p)


    def _add_task(self, info):
        self.taskList.add_task(info)


    def _remove_task(self, _id):
        self.taskList.remove_task(_id)


    def _disable_btns(self):
        self.resumeBtn.setDisabled(True)
        self.pauseBtn.setDisabled(True)
        self.removeBtn.setDisabled(True)


    def __task_menu_handler(self, data):
        info, pos = data

        is_completed = info.state == STATES.COMPLETED
        is_http = info._type == LINK_TYPE.HTTP

        options = [
            ('Open',            ACTIONS.OPEN,       is_completed),
            ('Show in folder',  ACTIONS.FOLDER,     is_completed),
            None,
            ('Copy Link',       ACTIONS.COPY_LINK,  True),
            None,
            ('Change URL',      ACTIONS.CHANGE_URL, is_http),
        ]

        self.menu, actions = self.__create_menu(options)

        action = self.menu.exec(pos)
        action = actions.get(action)

        if action:
            self.__send_request(info._id, action)


    def __create_menu(self, options):
        menu = QMenu(parent = self)
        actions = {}

        for option in options:
            if option:
                action = menu.addAction(option[0])
                action.setEnabled(option[2])
                actions[action] = option[1]
            else:
                menu.addSeparator()

        return menu, actions


    def __send_request(self, _id, action):
        self.requested.emit(_id, action)

