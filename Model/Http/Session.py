from threading import Thread, Lock
import time

from PyQt5.QtCore import QTimer

from Model.Util import run_task
from Utility.Core import STATES, STATUS
from Utility.Util import sizeChanger

from .Manager import Manager

# HTTP Session
class Session:

    THREAD_INDEX = 0
    MANAGER_INDEX = 1

    def __init__(self, setting = None):
        self.tasks = {}
        self.threads = {}
        self.garbages = []

        self.__running = False
        self.lock = Lock()

        self.__create_timer()

    

    def is_running(self):
        return self.__running
    
    def __set_running(self, state):
        self.lock.acquire()
        self.__running = state
        self.lock.release()
    

    def add_task(self, task):
        _id = task.get_id()
        self.tasks[_id] = task

    def remove_task(self, _id):
        self.lock.acquire()
        self.tasks.pop(_id, None)
        self.lock.release()


    def pause_task(self, _id):
        data = self.__get_thread(_id)
        if data:
            data[self.MANAGER_INDEX].pause()


    def resume_task(self, _id):
        if not self.__get_thread(_id):
            task = self.tasks.get(_id)

            if task:
                manager = self.__create_manager(task)

                thread = self.__create_thread(manager)
                self.threads[_id] = (thread, manager)

                manager.resume()
                thread.start()


    def __get_thread(self, _id):
        return self.threads.get(_id)


    def __create_manager(self, task):
        url = task.get_url()
        name = task.get_name()
        size = task.get_size()
        part = task.get_part()
        temp_path = task.get_temp_path()
        save_path = task.get_save_path()
        etag = task.get_etag()
        
        return Manager(url, name, size, part, temp_path, save_path, etag)


    def __create_thread(self, manager):
        return Thread(target = run_task, args = (manager,))


    def __remove_thread(self, _id):
        self.lock.acquire()

        data = self.threads.pop(_id, None)
        self.garbages.append(data)

        self.lock.release()
    

    def __move_to_garbage(self, data):
        self.garbages.append(data)


    def start(self):
        if not self.is_running():
            self.__set_running(True)
            self.__check_managers()
    
    def stop(self):
        self.__set_running(False)


    def __check_managers(self):

        count = 0
        max_opt = 50
        
        while self.is_running():
            _ids = list(self.threads.keys())

            remove = False
            
            for _id in _ids:

                task = self.__get_task(_id)
                manager = self.threads.get(_id)[self.MANAGER_INDEX]

                self.__update_task(task, manager)

                if manager.is_joining():
                    task.set_status(STATUS.BUILDING)
                else:
                    status = manager.get_status()
                    task.set_status(status)


                if manager.is_completed() or manager.is_paused():
                    
                    state = STATES.PAUSED
                    status = STATUS.PAUSED

                    if manager.is_completed():
                        state = STATES.COMPLETED
                        status = STATUS.COMPLETED

                        self.remove_task(task)
                    else:
                        if not task.is_paused():
                            status = manager.get_status()

                    task.set_state(state)
                    task.set_status(status)
                    self.__update_task(task, manager)

                    self.__remove_thread(_id)


            if count > max_opt:
                count = 0
                time.sleep(0.25)
            
            count += 1
        
        else:
            self.__stop_threads()
        

    def __stop_threads(self):
        
        for _, manager in self.threads.values():
            manager.pause()
        
        time.sleep(1)

        _ids = list(self.threads.keys())

        for _id in _ids:
            self.__remove_thread(_id)


    def __create_timer(self):
        self.__timer = QTimer()
        self.__timer.setSingleShot(False)
        self.__timer.timeout.connect(self.__dump_garbages)
        self.__timer.start(2000)


    def __dump_garbages(self):
        self.garbages.clear()


    def __get_task(self, _id):
        return self.tasks.get(_id)


    def __update_task(self, task, manager):
        downloaded = manager.get_downloaded()
        progress = manager.get_progress()
        speed = manager.get_speed()
        eta = manager.get_eta()

        task.set_eta(eta)
        task.set_down_speed(speed)
        task.set_progress(progress)
        task.set_downloaded(downloaded)

