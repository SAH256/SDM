import datetime as dt
import os

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt

from Utility.Core import ADD_STATE, HTTP, LINK_TYPE, CATEGORY, SETTING, ERRORS, TASK_TYPE, TASK_OPTIONS
from Utility.Util import split_file_name, sizeChanger, create_id, get_default_part
from Utility.Structure.Task.Torrent import TorrentOption
from Utility.Structure.Task.Http import HttpOption
from Utility.Structure.Task.Base import Request
from Utility.Gui import findCategory
from Utility.URL import url_type

from .AddUI import AddUI


# Add URL dialog -- Control class
class AddLink(AddUI):

    sendHead = QtCore.pyqtSignal(list)
    addTask = QtCore.pyqtSignal(list)

    def __init__(self, parent, queues, setting):
        super().__init__(parent)

        self.queues = queues
        self.setting = setting

        self.request = None
        self.response = None
        self.running = False
        self.added = False
        self.is_magnet = False

        self.__connect_slots()
        self.__toggle_magnet()
        self.__setup_menu()


    def __connect_slots(self):
        self.link_input.textChanged.connect(self.__link_handler)

        self.file_name.textChanged.connect(self.__check_file_name)
        self.extension.textChanged.connect(self.__extension_handler)

        self.torrent_option.info_changed.connect(self.__torrent_info_handler)

        self.save.path_changed.connect(self.__path_handler)
        self.category.category_changed.connect(self.__category_handler)

        self.cancelBtn.clicked.connect(self.close)
        self.startBtn.clicked.connect(self.__start_handler)

        self.advanceCheck.toggled.connect(self.__advance_handler)
    
    # setup dialog based on link and magnet case
    def __setup(self):
        name = TASK_TYPE.FILE
        category = CATEGORY.GENERAL

        if self.is_magnet:
            category = CATEGORY.TORRENT
            name = TASK_TYPE.TORRENT
        
        self.__toggle_magnet()
        self.__set_task_name(name)
        self.__set_error()
        self.__set_size(None)
        self.__set_running(False)
        self.category.set_category(category)

        if self.is_magnet:
            QtCore.QTimer.singleShot(200, self.__start_handler)
        self.__manage_btn_state()


    # create menu and add queue name as option
    def __setup_menu(self):
        menu = QtWidgets.QMenu(parent = self)
        menu.triggered.connect(self.__queue_handler)

        for queue in self.queues:
            menu.addAction(queue)
        
        self.addBtn.setMenu(menu)

    # show if we have send a request
    def is_running(self):
        return self.running

    # change running state for connecting situation
    def __set_running(self, state):
        self.running = state
        self.__setup_loading(state)
    

    def set_start_text(self, txt):
        self.startBtn.setText(txt)


    def enable_action_btns(self, state):
        self.startBtn.setEnabled(state)
        self.addBtn.setEnabled(state)


    def __toggle_magnet(self):
        self.file_name.setDisabled(self.is_magnet)
        self.extension.setDisabled(self.is_magnet)
        self.torrent_option.setVisible(self.is_magnet)
        self.seqCheck.setVisible(self.is_magnet)

        self.sliders.set_visible(part = not self.is_magnet, up = self.is_magnet)


    # toggle advance part of dialog
    def __advance_handler(self, state):
        self.category.setVisible(state)
        self.sliders.setVisible(state)
        self.auth.setVisible(state)

    # set dialog task type
    def set_header_name(self, name):
        self.name_header.setText(name)
        self.__update()


    # set error to error label
    def __set_error(self, txt = None):
        
        state = bool(txt)
        self.error_label.setVisible(state)

        if isinstance(txt, str):
            self.error_label.setText(txt)


    def set_link(self, link):
        self.link_input.set_text(str(link))



    def __link_handler(self):
        txt = self.link_input.text()
        self.is_magnet = url_type(txt) == LINK_TYPE.MAGNET
        
        self.__reset()


    # change start btn name by each state
    def __manage_btn_state(self):
        txt = None

        if self.is_running() or self.response:
            txt = ADD_STATE.START
        else:
            txt = ADD_STATE.CONNECT

        self.set_start_text(txt)


    # when start clicked which task must perform
    def __start_handler(self):

        if self.response or self.is_running():
            self.__add_task()
        else:
            self.__send_head()

        self.__manage_btn_state()


    # add link to client
    def __add_task(self):
        option = self.__get_option()
        self.added = True
        self.__send_add(option, start = True)


    # create request and send it to client
    def __send_head(self):
        state = False
        self.request = self.__create_request()

        if self.request:
            state = True
            self.__set_error()
            self.__send_request(self.request)
        else:
            # it must be find error
            self.__set_error(ERRORS.NO_LINK)

        self.__set_running(state)


    # send add link request with the data 
    # to add or discard it and start it immediately or not
    def __send_add(self, option, add = True, start = False):
        data = [option, add, start]
        self.addTask.emit(data)

        if self.added:
            self.close()


    # create request from data added to dialog
    def __create_request(self):
        link = self.link_input.text()
        _type = url_type(link)
        username = None
        password = None

        if self.auth.isChecked():
            username = self.auth.get_user()
            password = self.auth.get_password()


        if _type != None:
            _id = create_id(link, time_stamp = dt.datetime.now().timestamp())
            request = Request(_id, link, _type)
            request.user = username
            request.password = password

            return request


    # send fetch head request with response slot to client
    def __send_request(self, request):
        data = [request, self.__response_handler, True]
        self.sendHead.emit(data)
    

    # process response returned by client
    def __response_handler(self, response):
        
        if response.is_successful():
            self.response = response
            self.__setup_response()
        else:
            self.request = None
            self.__find_response_error(response)
    

        self.__set_running(False)
        self.__manage_btn_state()

        if not response.is_successful():
            self.enable_action_btns(False)



    # response is error then find error message
    def __find_response_error(self, response):
        message = response

        if not self.is_magnet:
            message = HTTP.RESPONSE.ERROR_STATUS.get(response.code)

        if message:
            self.__set_error(str(message))


    # request was successful now populate UI by response
    def __setup_response(self):
        if not self.response:
            return

        self.is_magnet = self.response._type == LINK_TYPE.MAGNET

        self.__toggle_magnet()

        self.__setup_file_name(self.response.name)
        self.__setup_size(self.response.size)

        if self.is_magnet:
            self.category.set_category(CATEGORY.TORRENT)
            self.torrent_option.set_data(self.response.file_info)
        else:
            part = get_default_part(self.response.size, self.response.resume)
            self.sliders.set_part(part)
        

    # set file name and extension
    def __setup_file_name(self, file_name):
        name = None
        ext = ''

        if self.is_magnet and self.response:
            name = file_name
        else:
            name, ext = split_file_name(file_name)
        

        self.__set_name(name)
        self.__set_ext(ext)


    def __set_name(self, name):
        self.file_name.set_text(name)
    
    def __set_ext(self, ext):
        self.extension.setText(ext)

    # size is an int change it to string and pass it to save box
    def __setup_size(self, size):
        txt = sizeChanger(size)

        self.save.set_size(size)
        self.__set_size(txt)


    def __set_size(self, txt = None):
        if not txt:
            txt = ''

        self.size_label.setText(txt)


    # if extension changed then change other part of UI
    def __extension_handler(self, txt):
        cat = CATEGORY.TORRENT

        if not self.is_magnet:
            cat = findCategory(txt.lower())

        self.__check_file_name()
        self.category.set_category(cat)


    # check if file name and extension are provided correctly or not
    def __check_file_name(self):
        state = True
        name = self.file_name.text()
        ext = self.extension.text()

        if self.response and not self.is_magnet:
            state = bool(name and ext)
        
        self.enable_action_btns(state)


    def __category_handler(self, category):
        setting = self.setting.get(SETTING.PATH)
        
        path = setting.get_path(category)

        self.save.set_path(path)


    def __path_handler(self):
        path = self.save.get_path()
        state = os.path.exists(path)

        self.enable_action_btns(state)


    def __get_link(self):
        return self.link_input.text()


    # change header task name
    def __set_task_name(self, name):
        if not name:
            return
        
        title = 'Add New ' + name

        self.setWindowTitle(title)
        self.set_header_name(name)

    # option from queue menu selected then create option and send it 
    def __queue_handler(self, action):
        name = action.text()
        option = self.__get_option()

        if option:
            option.queue = name
            self.added = True
            self.__send_add(option)


    def __create_option(self, _type, _id = None):
        option = None

        if _type == LINK_TYPE.HTTP:
            option = HttpOption(_id)
        else:
            option = TorrentOption(_id)

        return option


    # create option from request/response and other data from UI
    def __get_option(self):
        if not self.__get_link():
            return

        if not self.request:
            self.request = self.__create_request()

        
        _id = self.request.get_id()
        _type = self.request.get_type()
        option = self.__create_option(_type, _id)


        if _type == LINK_TYPE.HTTP:

            option.url = self.request.url
            option.name = self.__get_file_name()
            option.part = self.sliders.get_part()
            option.username, option.password = self.__get_auth()

            if self.response:
                option.url = self.response.url
                option.size = self.response.size
                option.resume = self.response.resume
                option.etag = self.response.etag
                option.modified_date = self.response.date


        else:
            option.up_limit = self.sliders.get_up_limit()
            option.sequential = self.seqCheck.isChecked()

            if self.response:
                option.file_info = self.response.file_info

            # option.trackers = ...                                 it will complete in future


        if self.response:
            option.metadata = True



        option.category = self.category.get_category()
        option.queue = self.queues[0]
        option.path = self.save.get_path()
        option.date = dt.datetime.now().timestamp()
        option.down_limit = self.sliders.get_down_limit()

        option.options = {
            TASK_OPTIONS.PROXY : self.proxyCheck.isChecked(),
            TASK_OPTIONS.RETRY : self.retryCheck.isChecked(),
            TASK_OPTIONS.HIDDEN : self.hiddenCheck.isChecked(),
        }



        return option



    def __get_file_name(self):
        
        name = self.file_name.text()
        ext = self.extension.text()

        if not self.is_magnet and ext:
            name = f'{name}.{ext}'
        
        return name
    

    def __get_auth(self):
        user, password = None, None

        if not self.is_magnet and self.auth.isChecked():
            user = self.auth.get_user()
            password = self.auth.get_password
        
        return user, password


    # reset dialog to default
    def __reset(self):
        self.request = None
        self.response = None

        self.__set_running(False)
        self.__notify_client()

        for wid in self.widgets:
            if hasattr(wid, '_reset'):
                wid._reset()

        self.__setup()
        self.__setup_loading(False)



    # this is only for updating header label
    def __update(self):
        self.style().unpolish(self.name_header)
        self.style().polish(self.name_header)
        self.update()
    

    # send empty option to client for discarding any request or task
    def __notify_client(self):
        if self.request and not self.added:
            option = self.__create_option(self.request.get_type(), self.request.get_id())
            self.__send_add(option, False, False)


    # set torrent metadata to its widget
    def __torrent_info_handler(self):
        if self.response:
            size = self.response.file_info.get_size()
            self.__setup_size(size)


    # setup loading gif label
    def __setup_loading(self, state):
        self.loading.setVisible(state)

        if state:
            self.loading.start()
        else:
            self.loading.stop()


    def closeEvent(self, ev):
        self.__notify_client()
        super().closeEvent(ev)


