from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

from UI.Base.Menu.StyledMenu import StyleMenu

from UI.Main.Add.AddControl import AddLink
from UI.Main.About.AboutControl import About
from UI.Main.Batch.BatchControl import BatchControl
from UI.Main.Group.GroupControl import GroupControl
from UI.Main.Popup.PopupControl import create_popup
from UI.Main.Scheduler.SchedulerControl import Scheduler
from UI.Main.Setting.SettingControl import Setting as SettingDialog

from UI.Torrent.Magnet.AddMagnetControl import AddMagnetControl
from UI.Torrent.TorrentSetting.TorrentControl import TorrentControl

from Utility.Core import ICONS, CATEGORY, ACTIONS, FILTER, STATUS, STATES, POPUP_TYPE, LINK_TYPE, SELECTORS
from Utility.Structure.Task.Base import ActionRequest
from Utility.Actions import turn_off
from Utility.URL import url_type

from .mainUIControl import UIControl


# Main Window of GUI
class MainWindow(QtWidgets.QMainWindow):

    user_exited = pyqtSignal()

    def __init__(self, client, setting):
        super().__init__()

        self.client = client
        self.setting = setting

        self.__user_exit = False

        w, h = 800, 600
        self.resize(w, h)
        
        title = 'Simple Download Manager'
        self.setWindowTitle(title)

    def setup(self):
        self.__central_widget()
        self.__setup_categories()
        self.__setup_left_menu()
        self.__setup_headers()
        self.__setup_actions()
        self.__queue_menu()
        self.__setup_menubar()

        self.__connect_slots()


    def __central_widget(self):
        self.central_widget = UIControl(self)
        self.setCentralWidget(self.central_widget)

        for info in self.client.get_all_info():
            self.central_widget._add_task(info)


    def __setup_categories(self):
        items = [
            (ICONS.CATEGORY.ALL_DOWN, 'All Downloads', None),
            (ICONS.CATEGORY.COMPRESSED, CATEGORY.COMPRESSED),
            (ICONS.CATEGORY.PROGRAM, CATEGORY.PROGRAM),
            (ICONS.CATEGORY.AUDIO, CATEGORY.AUDIO),
            (ICONS.CATEGORY.IMAGE, CATEGORY.IMAGE),
            (ICONS.CATEGORY.VIDEO, CATEGORY.VIDEO),
            (ICONS.CATEGORY.DOCUMENT, CATEGORY.DOCUMENT),
            (ICONS.CATEGORY.TORRENT, CATEGORY.TORRENT),
            (ICONS.CATEGORY.GENERAL, CATEGORY.GENERAL),
        ]

        self.central_widget.add_categories(items)


    def __setup_left_menu(self):
        left_tools = [
            (ICONS.ANIMATION.SETTING, 'Application Setting', self.__setting_handler),    
        ]

        self.central_widget.add_left_tools(left_tools)


    def __setup_headers(self):
        header_items = [
            (ICONS.HEADER.ALL,          'All',          FILTER.STATUS, [None, None]),
            (ICONS.HEADER.DOWNLOADING,  'Downloading',  FILTER.STATUS, [STATES.RUNNING,   True]),
            (ICONS.HEADER.FINISHED,     'Finished',     FILTER.STATUS, [STATES.COMPLETED, None]),
            (ICONS.HEADER.UNFINISHED,   'Unfinished',   FILTER.STATUS, [(STATES.COMPLETED,),    None]),
            (ICONS.HEADER.ERROR,        'Error',        FILTER.STATUS, [STATES.PAUSED,    False]),
        ]

        self.central_widget.add_headers(header_items)


    def __setup_actions(self):
        actions = {
            ('addBtn', True) :            (ICONS.ACTION.ADD, 'Add Download', 'Add new download', self.__add_handler),
            ('addMagnetBtn', True) :      (ICONS.ACTION.MAGNET, 'Add &Torrent', 'Add new torrent', self.__open_magnet),
            ('resumeBtn', False) :        (ICONS.ACTION.RESUME, 'Resume', 'Resume selected tasks', self.__resume_handler),
            ('pauseBtn', False) :         (ICONS.ACTION.PAUSE, 'Pause', 'Pause selected tasks', self.__pause_handler),
            ('removeBtn', False) :        (ICONS.ACTION.REMOVE, 'Remove', 'Delete selected tasks', self.__remove_handler),
            ('schedulerBtn', True) :      (ICONS.ACTION.SCHEDULER, 'Scheduler', 'Schedule your tasks', self.__scheduler_handler),
            ('startBtn', True) :          (ICONS.ACTION.START, 'Start Queue', 'Start queue actions', self.__start_queue_handler),
            ('stopBtn', True) :           (ICONS.ACTION.STOP, 'Stop Queue', 'Stop queue actions', self.__stop_queue_handler),
            ('torrentSettingBtn', True) : (ICONS.ACTION.TORRENT_SETTING, 'Torrent Setting', 'Manage your torrent tasks', self.__torrent_setting_handler),
        }

        items_data = {}

        for info, data in actions.items():
            icon = data[0]
            name = data[1]
            tip = data[2]
            handler = data[3]

            action = QtWidgets.QAction(name, toolTip = tip, triggered = handler)

            items_data[info] = icon, action

        self.central_widget.add_actions(items_data)


    def __queue_menu(self):
        self.queue_menu = StyleMenu()
        self.queue_menu.triggered.connect(self.__queue_handler)
        self.__populate_menu()
        self.__manage_queue_header()


    # manage queue that appear in header section
    def __manage_queue_header(self):
        queues = self.client.get_queues()
        headers = []

        for queue in queues:
            if self.central_widget.headerTab.exist(queue) < 0:
                item = (ICONS.HEADER.QUEUE, queue, FILTER.QUEUE, queue)
                headers.append(item)

        if headers:
            self.central_widget.add_headers(headers)

        self.central_widget.headerTab.check_queues(queues)


    def __start_queue_handler(self):
        point = self.central_widget.startBtn.mapToGlobal(QPoint(0, 0))
        width = 190
        point.setX(point.x() - width)
        self.__populate_menu()

        self.queue_menu.popup(point)


    def __stop_queue_handler(self):
        point = self.central_widget.stopBtn.mapToGlobal(QPoint(0, 0))
        width = 190
        point.setX(point.x() - width)
        self.__populate_menu(False)

        self.queue_menu.popup(point)


    def __populate_menu(self, is_start = True):
        manager = self.client.get_queue_manager()
        states = manager.get_state()

        for action in self.queue_menu.actions():
            self.queue_menu.removeAction(action)

        for name, state in states:
            action = self.queue_menu.addAction(name)
            action.setEnabled(is_start != state)


    def __queue_handler(self, action):
        queue = action.text()
        manager = self.client.get_queue_manager()
        queue = manager.get_queue(queue)

        if queue:
            if queue.is_running():
                queue.stop_action()
            else:
                queue.start_action()


    def __setup_menubar(self):
        menus = {
            'File' : [
                ('New Download', self.__add_handler),
                ('New Torrent', self.__open_magnet),
                ('Batch Download', self.__open_batch),
                None,
                ('Exit', self.close)
            ],

            'Downloads' : [
                ('Pause All', self.__pause_all_handler),
                ('Resume All', self.__resume_all_handler),
                None,
                ('Remove All Finished', self.__remove_finished_handler),
            ],

            'Controls' : [
                ('Scheduler', self.__scheduler_handler),
                ('Torrent Setting', self.__torrent_setting_handler),
            ],

            'Help' : [
                ('About', self.__open_about),
            ]
        }

        for title in menus:
            menu = self.menuBar().addMenu(title)

            for item in menus[title]:
                if item:
                    action = menu.addAction(item[0])
                    action.triggered.connect(item[1])
                else:
                    menu.addSeparator()


    def __connect_slots(self):
        self.client.requested.connect(self.__system_request_handler)
        self.central_widget.requested.connect(self.__action_request_handler)


    def __system_request_handler(self, data):
        if data:
            if data[1]:
                turn_off(*data[1:])

            if data[0]:
                self.__user_exit = True
                self.close()


    def __add_handler(self):
        url = None
        _type, text = self.__get_url_from_clipboard()

        if _type:
            url = text

        self.__open_add(url)


    def __open_add(self, url = None):
        setting = self.setting.get_client_setting()

        d = AddLink(self, self.client.get_queues(), setting)
        c1 = d.sendHead.connect(self.__head_request_handler)
        c2 = d.addTask.connect(self.__task_handler)

        if url:
            d.set_link(url)

        d.exec()

        d.sendHead.disconnect(c1)
        d.addTask.disconnect(c2)
    

    def __head_request_handler(self, data):
        request = data[0]
        slot = data[1]
        is_single = data[2]

        if is_single:
            self.client.fetch_metadata(request, slot)
        else:
            self.client.fetch_multi(request, slot)


    def __open_magnet(self):
        d = AddMagnetControl(self)
        c = d.sendData.connect(self.__open_add)
        d.exec()

        d.sendData.disconnect(c)


    def __task_handler(self, data):
        option = data[0]
        add = data[1]
        start = data[2]
        duplicate_option = None

        if add:
            add, duplicate_option = self.__check_duplicate(option)

        info = self.client.add_task(option, add, start, duplicate_option)

        if info:
            self.central_widget._add_task(info)


    def __open_batch(self):
        d = BatchControl(self)
        connection = d.sendRequest.connect(self.__open_group)

        _type, url = self.__get_url_from_clipboard()

        if _type and _type == LINK_TYPE.HTTP:
            d.set_link(url)

        d.exec()

        d.sendRequest.disconnect(connection)


    def __open_group(self, request_data):

        setting = self.setting.get_path()

        d = GroupControl(self, self.client.get_queues(), setting)

        c1 = d.sendHead.connect(self.__head_request_handler)
        c2 = d.addTasks.connect(self.__add_group_handler)

        d.add_batch_data(request_data)
        d.exec()

        d.sendHead.disconnect(c1)
        d.addTasks.disconnect(c2)
        d.deleteLater()



    def __add_group_handler(self, option_list):

        for op in option_list:
            self.__task_handler([op, True, False])


    def __pause_handler(self):
        self.central_widget._toggle_action_btn()

        items = self.central_widget.get_selected()

        for item in items:
            self.client._pause_task(item)


    def __resume_handler(self):
        self.central_widget._toggle_action_btn()

        items = self.central_widget.get_selected()

        for item in items:
            self.client._resume_task(item)


    def __remove_handler(self):
        
        items = self.central_widget.get_selected()

        if items:
            self.__remove_items(items)


    def __remove_items(self, items):
        if items:
            names = []

            for _id in items:
                info = self.client.get_task_info(_id)

                if info:
                    names.append(info.name)

            is_finished = False

            _type = POPUP_TYPE.DELETE
            title = 'Remove Task(s)'

            result = create_popup(self, _type, title, SELECTORS.STATES.DANGER, [names, is_finished])

            if result[0]:
                for item in items:
                    self.client._remove_task(item, result[1])
                    self.central_widget._remove_task(item)

                self.central_widget._disable_btns()


    def __torrent_setting_handler(self):
        d = TorrentControl(self, self.client.get_torrents_info())
        c = d.item_requested.connect(self.__action_request_handler)
        d.exec()
        d.item_requested.disconnect(c)


    def __action_request_handler(self, _id, action):

        request = ActionRequest(_id, action)

        if action == ACTIONS.SAVE_TORRENT:
            path = self.__select_path()
            request.data = path

            # dont send request
            if not path:
                return

        elif action == ACTIONS.CHANGE_URL:

            info = self.client.get_task_info(_id)

            _type = POPUP_TYPE.TEXTAREA
            title = 'Change URL'

            result = create_popup(self, _type, title, SELECTORS.STATES.PLAIN, info.url)

            if result:
                request.data = result
            else:
                return

        self.client._request_handler(request)


    def __scheduler_handler(self):
        d = Scheduler(self, self.client.get_queue_manager())
        req = d.exec()

        self.__manage_queue_header()


    def __check_duplicate(self, option):
        duplicate_option = True

        _type = option._type

        if _type == LINK_TYPE.HTTP:
            has_duplicate = self.client.has_duplicate(option.url, _type)

            if has_duplicate:
                duplicate_option = self.__popup_options(option.url)
        else:
            duplicate_option = False if self.client.get_task(option._id) else True

        return bool(duplicate_option), duplicate_option


    def __popup_options(self, link):
        _type = POPUP_TYPE.DUPLICATE
        title = 'Duplicate URL Found'

        option = create_popup(self, _type, title, data = link)

        return option


    def __select_path(self):
        text = 'Select path to save'
        path = QtWidgets.QFileDialog.getExistingDirectory(caption = text)

        return path


    def __setting_handler(self):
        d = SettingDialog(self, self.setting)
        d.exec()


    def __open_about(self):
        d = About(self)
        d.exec()


    def __pause_all_handler(self):
        self.client._pause_all()


    def __resume_all_handler(self):
        self.client._resume_all()


    def __remove_finished_handler(self):
        _type = POPUP_TYPE.DELETE
        title = 'Remove Tasks'
        is_finished = True

        result = create_popup(self, _type, title, SELECTORS.STATES.DANGER, [None, is_finished])

        if result[0]:
            deleted_tasks = self.client._remove_all_finished(result[1])
            [self.central_widget._remove_task(_id) for _id in deleted_tasks]


    def __get_url_from_clipboard(self):
        url = QtWidgets.QApplication.clipboard().text()
        return url_type(url), url


    # def __close_handler(self, system = True):
    #     if not system:
    #         self.user_exited.emit()

    #     self.close()


    def closeEvent(self, ev):
        self.client.stop_session()

        self.user_exited.emit()

        super().closeEvent(ev)


