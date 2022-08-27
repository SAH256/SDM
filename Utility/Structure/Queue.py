from threading import Lock

from PyQt5.QtCore import QTimer

from Utility.Core import QUEUE


# Queue Timer class
class Timer:

    def __init__(self):

        self.start_time = None
        self.timer_basis = {QUEUE.TIMER.DATE : None, QUEUE.TIMER.REPEAT : None, QUEUE.TIMER.DAY : None}
        self.stop_time = None
    
    def _get_save_data(self):
        return [
            self.start_time,
            self.stop_time,
            self.timer_basis
        ]
    
    def _set_save_data(self, data):
        if data:
            self.start_time, self.stop_time, self.timer_basis = data




# Queue File manager class
class File:

    def __init__(self):

        self.tasks = []
        self.lock = Lock()


    def add_task(self, task):
        self.lock.acquire()

        if task not in self.tasks:
            _id = task.get_id()

            if _id in self.tasks:
                self.tasks[self.tasks.index(_id)] = task
            else:
                self.tasks.append(task)

        self.lock.release()
    

    def get_task(self, suspends):

        for task in self.tasks:
            if type(task) is str:
                continue

            if task.is_paused() and not task.is_completed() and task not in suspends:
                return task

    def has_task(self, task):
        index = -1

        try:
            index = self.tasks.index(task)
        except ValueError:
            pass
        
        return index > -1

    def set_status(self, status):
        for task in self.tasks:
            task.set_status(status)

    def count(self):
        return len(self.tasks)

    def get_info(self):
        self.lock.acquire()
        data = [x.get_info() for x in self.tasks if type(x) != str]
        self.lock.release()

        return data

    def change_order(self, pattern):
        
        self.lock.acquire()

        for task in self.tasks:

            if pattern.count(task.get_id()):
                ind = pattern.index(task.get_id())
                pattern[ind] = task
        
        self.tasks = pattern

        self.lock.release()
    

    def remove_task(self, task):
        self.lock.acquire()

        if self.has_task(task):
            self.tasks.remove(task)

        self.lock.release()


    def remove_tasks(self, items):

        self.lock.acquire()

        ids = [x.get_id() for x in self.tasks]
        data = []

        for item in items:
            if item in ids:
                ind = ids.index(item)
                task = self.tasks.pop(ind)
                task.set_queue(None)
                ids.pop(ind)

                data.append(task)

        self.lock.release()
    
        return data
    

    def reset(self):
        for task in self.tasks:
            task.set_queue(None)
        
        self.tasks.clear()
    

    def _get_save_data(self):
        return [x._id for x in self.get_info()]
    
    def _set_save_data(self, data):
        self.tasks.extend(data)


# Queue Process class
class Process:

    def __init__(self):

        s = QUEUE.PROCESS.SUB
        self.sub_process = {s.MOVE_DIR: False, s.MOVE_END: False, s.BEEP: False}

        p = QUEUE.PROCESS.POST
        self.post_process = {
            p.OPEN_FILE: False,
            p.EXIT_APP: False,
            p.TURN_OFF: False,
            p.FORCE_SHUT_DOWN: False
        }
    
    def _get_save_data(self):
        return [
            self.sub_process,
            self.post_process
        ]
    
    def _set_save_data(self, data):
        if data:
            self.sub_process, self.post_process = data



# Queue Setting class
class QueueSetting:

    def __init__(self, name, timer_type, creator_type):
        self.name = name
        self.timer_type = timer_type
        self.creator_type = creator_type
        self.concurrent = 1
        self.startup = False
        self.retry = 0
    
    def _get_save_data(self):
        return [
            self.concurrent,
            self.startup,
            self.retry
        ]
    
    def _set_save_data(self, data):
        if data:
            self.concurrent, self.startup, self.retry = data




