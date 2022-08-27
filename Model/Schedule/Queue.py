import datetime as dt
from threading import Lock

from PyQt5 import QtCore

from Utility.Structure.Queue import Timer, File, Process, QueueSetting
from Utility.Structure.Task.Base import ActionRequest
from Utility.Core import QUEUE, STATUS, ACTIONS
from Utility import Calcs as calcs, Actions


class Queue(QtCore.QObject):

    action_requested = QtCore.pyqtSignal(ActionRequest)

    def __init__(self, name, timer_type, creator_type):
        super().__init__()

        self.timer = Timer()
        self.files = File()
        self.process = Process()
        self.setting = QueueSetting(name, timer_type, creator_type)

        self.lock = Lock()

        self.running = False
        self.__interval = None
        self.request = None

        self.actives = []
        self.suspends = []

        self.__manage_reset()
    

    def get_creator_type(self):
        return self.setting.creator_type

    def get_timer_type(self):
        return self.setting.timer_type
    
    def get_name(self):
        return self.setting.name

    def add_task(self, task):
        task.set_queue(self.get_name())
        self.files.add_task(task)

    def remove_task(self, task):
        self.files.remove_task(task)


    def remove_tasks(self, items):
        return self.files.remove_tasks(items)

    def has_task(self, task):
        return self.files.has_task(task)


    def is_running(self):
        return self.running

    # start queue for controlling downloads
    def start_action(self):

        self.__manage_interval()
        self.request = None

        if self.files.count() and not self.is_running():
            self.__set_running(True)
            self.files.set_status(STATUS.QUEUED)
            self.__setup_update()


    def __manage_interval(self):
        if self.__interval and self.__start_timer.interval() != self.__interval:
            self.__start_timer.setInterval(self.__interval)
            self.__interval = None


    def __setup_update(self):
        self.__update_timer = QtCore.QTimer()
        self.__update_timer.timeout.connect(self.__manage_tasks)
        self.__update_timer.setSingleShot(False)
        self.__update_timer.start(1000)


    def __set_running(self, s = False):
        self.lock.acquire()
        self.running = s
        self.lock.release()
        

    def __manage_tasks(self):
        if not self.is_running():
            return

        # checking tasks status
        for task in self.actives:
            perform = False

            if task.is_paused():
                self.actives.remove(task)
                self.suspends.append(task)
                perform = True

            elif task.is_completed():

                self.actives.remove(task)
                self.files.remove_task(task)
                perform = True
            
            if perform:
                self.__perform_sub(task)


        while len(self.actives) < self.setting.concurrent:
            task = self.files.get_task(self.suspends)

            if task:
                self.actives.append(task)
                self.__send_action_request(task.get_id(), ACTIONS.RESUME)
            else:
                break
        
        self.__check_stop()


    def __check_stop(self):
        stop = False
        perform = False
        
        # no active task and no possible task
        if len(self.actives) == 0 and not self.files.get_task(self.suspends):
            stop = True
            perform = True

        if self.timer.stop_time and calcs.time_passed(dt.time.fromisoformat(self.timer.stop_time)):
            
            self.__start_timer.stop()
            del self.__start_timer
            
            stop = True
        
        if stop:
            self.stop_action()

            if perform:
                self.__perform_post()


    def stop_action(self):
        self.__set_running(False)

        # for each task perform its process
        for task in self.actives:
            if task.is_completed() or task.is_paused():
                self.__perform_sub(task)
            else:
                self.__send_action_request(task.get_id(), ACTIONS.PAUSE)

        self.actives.clear()
        self.suspends.clear()
        self.files.set_status(STATUS.PAUSED)

        self.__update_timer.stop()

    
    def __send_action_request(self, _id, action, data = None):
        request = ActionRequest(_id, action)
        request.data = data
        
        self.action_requested.emit(request)


    def __perform_sub(self, task):
        # THIS MUST FILLED IN FUTURE UPDATES...
        pass


    def __perform_post(self):
        post = self.process.post_process
        p = QUEUE.PROCESS.POST
        _dir = post.get(p.OPEN_FILE)

        if _dir:
            Actions.open_file(_dir)

        data = [post.get(p.EXIT_APP), post.get(p.TURN_OFF), post.get(p.FORCE_SHUT_DOWN)]
        action = ACTIONS.SYSTEM

        if True in data:
            self.__send_action_request(None, action, data)


    # setup start timer for queue based on timer data
    def setup_timer(self):
        
        if hasattr(self, '__reset_timer'):
            self.__reset_timer.setInterval(86400 * 1000)

        start = False
        interval = None

        if self.timer.start_time:
            timer_date = self.timer.timer_basis.get(QUEUE.TIMER.DATE)

            if self.get_timer_type() == QUEUE.SETTING.ONE_TIME and timer_date:
                if calcs.is_today(timer_date, dt.time.fromisoformat(self.timer.start_time)):
                    start = True

            else:
                days = self.timer.timer_basis.get(QUEUE.TIMER.DAY)
                if days.get(calcs.get_today_week()):
                    start = True

            repeat = self.timer.timer_basis.get(QUEUE.TIMER.REPEAT)

            if self.get_timer_type() == QUEUE.SETTING.PERIODIC and repeat:
                interval = calcs.change_to_micro(repeat)


            if start:
                self.__start_timer = QtCore.QTimer()
                self.__start_timer.timeout.connect(self.start_action)

                self.__start_timer.setSingleShot(not bool(interval))
                
                if interval:
                    self.__interval = interval

                self.__start_timer.setTimerType(QtCore.Qt.TimerType.PreciseTimer)
                
                d = calcs.difference_time(dt.time.fromisoformat(self.timer.start_time))
                
                self.__start_timer.start(d)


    def __manage_reset(self):
        self.__reset_timer = QtCore.QTimer()
        self.__reset_timer.timeout.connect(self.setup_timer)
        self.__reset_timer.setSingleShot(False)
        self.__reset_timer.start(calcs.until_midnight())


    def reset(self):
        self.files.reset()


    def _set_save_data(self, timer, files, process, setting):
        self.timer._set_save_data(timer)
        self.files._set_save_data(files)
        self.process._set_save_data(process)
        self.setting._set_save_data(setting)

        self.setup_timer()


    def _get_save_info(self):
        return (self.get_timer_type(), self.get_creator_type()), self.timer._get_save_data(), self.files._get_save_data(), self.process._get_save_data(), self.setting._get_save_data()



