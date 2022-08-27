import os

from PyQt5 import QtCore

from Utility.Core import SDM, ACTIONS, STATES, STATUS, SAVES, TASK_OPTIONS
from Utility.Structure.Task.Base import TaskInfo, ActionRequest


class BaseTask(QtCore.QObject):

    action_requested = QtCore.pyqtSignal(ActionRequest)

    def __init__(self, _id):
        super().__init__()

        self.info = TaskInfo()

        self.set_id(_id)

        self.options = {x : False for x in TASK_OPTIONS.TEXT}
        self.paused = True
        self.running = False


    def setup(self, option):
        self.set_queue(option.queue)
        self.set_category(option.category)
        self.set_save_path(option.path)
        self.set_downloaded(option.downloaded)
        self.set_progress(option.progress)
        self.__set_options(option.options)
        self.pause()

        if option.date:
            self.set_date(option.date)


        state = STATES.PAUSED
        status = STATUS.PAUSED

        if option.state == STATES.COMPLETED:
            state = option.state
            status = STATUS.COMPLETED


        self.set_status(status)
        self.set_state(state)


    # set task attribute options
    def __set_options(self, options):
        for key, value in options.items():
            if self.options.get(int(key)) != None:
                self.options[int(key)] = value

    
    def pause(self):
        self.paused = True
        self.set_state(STATES.PAUSED)
        self.action_requested.emit(self._create_request(ACTIONS.PAUSE))

    def resume(self):
        self.paused = False
        self.set_state(STATES.RUNNING)
        self.action_requested.emit(self._create_request(ACTIONS.RESUME))
    
    def remove(self):
        self.action_requested.emit(self._create_request(ACTIONS.REMOVE))

    def is_running(self):
        return self.running
    
    def is_paused(self):
        return self.paused
    
    def is_completed(self):
        return (self.get_size() > 0) and (self.info.downloaded == self.info.total_size) and (self.get_state() == STATES.COMPLETED)

    def set_resume(self, data):
        self.info.resume = data

    def get_state(self):
        return self.info.state

    def set_state(self, state):

        if state != self.get_state():
            self.info.state = state

    def set_status(self, status):
        if status != self.get_status():
            self.info.status = status

    
    def get_status(self):
        return self.info.status


    def set_name(self, name):
        self.info.name = name

    def set_downloaded(self, d):
        self.info.downloaded = d

    def get_downloaded(self):
        return self.info.downloaded

    def set_size(self, size):
        self.info.total_size = size
    
    def get_size(self):
        return self.info.total_size

    def get_name(self):
        return self.info.name
    
    def get_type(self):
        return self.info._type
    
    def set_type(self, _type):
        self.info._type = _type
    
    def get_queue(self):
        return self.info.queue

    def set_save_path(self, path):
        self.info.path = path

    def get_save_path(self):
        return self.info.path
    
    def get_dirname(self):
        return os.path.join(self.get_save_path(), self.get_name())

    def set_category(self, category):
        self.info.category = category

    def get_category(self):
        return self.info.category

    def get_id(self):
        return self.info._id
    
    def set_id(self, _id):
        self.info._id = _id

    def get_info(self):
        return self.info
    
    def has_metadata(self):
        return self.info.metadata

    def set_metadata(self, state):
        self.info.metadata = state    

    def set_progress(self, progress):
        self.info.progress = progress


    def get_progress(self):
        return self.info.progress


    def set_queue(self, q):
        self.info.queue = q

    def set_date(self, date):
        self.info.date = date
    
    def get_date(self):
        return self.info.date

    def get_temp_path(self):
        return os.path.join(SDM.PATHS.TEMP_PATH, self.get_id())

    def _create_request(self, action):
        return ActionRequest(self.get_id(), action)

    def set_down_speed(self, speed):
        self.info.download_speed = speed

    def set_eta(self, eta):
        self.info.eta = eta

    def get_down_limit(self):
        pass


    def _get_save_data(self):
        return {
            SAVES.SLOTS.ID :         self.get_id(),
            SAVES.SLOTS.NAME :       self.get_name(),
            SAVES.SLOTS.QUEUE :      self.get_queue(),
            SAVES.SLOTS.CATEGORY :   self.get_category(),
            SAVES.SLOTS.PATH :       self.get_save_path(),
            SAVES.SLOTS.DATE :       self.get_date(),
            SAVES.SLOTS.METADATA :   self.has_metadata(),
            SAVES.SLOTS.DOWNLOADED : self.get_downloaded(),
            SAVES.SLOTS.PROGRESS :   self.get_progress(),
            SAVES.SLOTS.SIZE :       self.get_size(),
            SAVES.SLOTS.STATE :      self.get_state(),
            SAVES.SLOTS.DOWN_LIMIT : self.get_down_limit(),
            SAVES.SLOTS.OPTIONS :    self.options,
        }




