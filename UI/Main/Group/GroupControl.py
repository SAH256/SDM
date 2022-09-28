import datetime as dt

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

from UI.Base.Menu.StyledMenu import StyleMenu

from Utility.Structure.Task.Http import MultiRequest, LinkGenerator, HttpOption
from Utility.Util import sizeChanger, create_id, split_file_name
from Utility.URL import find_filename
from Utility.Gui import findCategory

from .GroupUI import GroupUI


# Group dialog -- Control class
class GroupControl(GroupUI):
    
    sendHead = pyqtSignal(list)
    addTasks = pyqtSignal(list)
    
    def __init__(self, parent, queue_list, setting):
        super().__init__(parent)
        
        self.path_setting = setting
        self.queue_list = queue_list

        self.name_pattern = ''
        self.wildcard = '*'

        self.running = False

        self.__connect_slots()
        self.__manage_queue_menu()
        self.__setup()


    def __connect_slots(self):
        self.allCheck.toggled.connect(self.__select_handler)
        self.itemList.selection_changed.connect(self.__info_handler)
        self.nameBox.textChanged.connect(self.__name_handler)
        self.cancelBtn.clicked.connect(self.close)


    def __manage_queue_menu(self):
        menu = StyleMenu(parent = self)
        menu.triggered.connect(self.__add_handler)

        for name in self.queue_list:
            menu.addAction(name)

        self.addBtn.setMenu(menu)


    def __setup(self):
        self.saveBox.set_setting(self.path_setting)


    def add_batch_data(self, request_data):
        if not request_data:
            return

        self.request_data = request_data

        generator = LinkGenerator(*request_data)

        name = ''

        for _id, link in generator.info_iter():
            self.__add_item(_id)

        pattern = find_filename(request_data[0])
        self.__setup_pattern(pattern)

        self.__send_request(request_data[0], generator.request_iter())


    def is_running(self):
        return self.running


    def __set_running(self, state):
        self.running = state


    def __add_item(self, item_info):
        self.itemList.add_item(item_info)


    def __create_request(self, url):
        _id = create_id(url, time_stamp = dt.datetime.now().timestamp())

        return MultiRequest(_id)


    def __send_request(self, url, link_iter):
        request = self.__create_request(url)
        request.set_link_iter(link_iter)

        self.__send_signal(request)


    def __send_signal(self, request):
        data = [request, self.__response_handler, False]
        self.sendHead.emit(data)


    def __response_handler(self, data):
        _id = data[0]
        metadata = data[1]

        self.itemList.set_data(_id, metadata)


    def __setup_pattern(self, pattern):
        self.nameBox.setText(pattern.replace('{}', '*'))


    def __info_handler(self, data):
        count = data[1]

        size = sizeChanger(data[0])
        text = f'{count} file{"s" if count > 1 else ""} ({size})'
        self.sizeBox.setText(text)


    def __name_handler(self, text):
        if text.count(self.wildcard):
            text = text.replace(self.wildcard, '{}')
            self.name_pattern = text
            self.itemList.set_pattern(text)


    def __select_handler(self, state):
        self.itemList.select_all(state)


    def __add_handler(self, action):
        queue = action.text()

        path = self.saveBox.get_path()
        selected_data = self.itemList.get_data()

        part = self.sliderPane.get_part()
        limit = self.sliderPane.get_down_limit()

        auth = self.request_data[-2:]
        options = []

        for _id, metadata in selected_data.items():

            date = dt.datetime.now().timestamp()

            new_id = create_id(metadata.url, time_stamp = date)

            op = HttpOption(new_id)

            if metadata:
                op.url = metadata.url
                op.size = metadata.size
                op.resume = metadata.resume
                op.etag = metadata.etag
            else:
                op.url = self.request_data[0].format(_id)

            if auth:
                op.username = auth[0]
                op.password = auth[1]

            op.metadata = bool(metadata)

            op.name = self.name_pattern.format(_id)
            op.queue = queue
            op.date = date
            op.part = part
            op.down_limit = limit

            ext = split_file_name(op.name)[-1]
            op.category = findCategory(ext)

            if path:
                op.path = path
            else:
                op.path = self.path_setting.get_path(op.category)

            options.append(op)

        self.addTasks.emit(options)
        self.close()




