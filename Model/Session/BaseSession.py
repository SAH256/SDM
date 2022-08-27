from PyQt5 import QtCore

from Model.Task.Base import BaseTask

from Utility.Core import ACTIONS
from Utility.Actions import makeTempDir


# base session class 
class BaseSession(QtCore.QObject):
    
    def __init__(self, setting = None):
        super().__init__()
        
        self.setting = setting
        self.tasks = {}
        self.running = False
    

    def add_task(self, task):
        if isinstance(task, BaseTask) and task.get_id() not in self.tasks:
            
            self.tasks[task.get_id()] = task
            makeTempDir(task.get_id())

            task.action_requested.connect(self._task_request_handler)


    # handle UI request in the session
    def _task_request_handler(self, request):

        action = request.get_action()

        if action == ACTIONS.PAUSE:
            self.pause_task(request)
        elif action == ACTIONS.RESUME:
            self.resume_task(request)
        elif action == ACTIONS.REMOVE:
            self.remove_task(request)
    

    def pause_task(self, request):
        pass

    def resume_task(self, request):
        pass

    def remove_task(self, request):
        pass

    def pause(self):
        self.running = False
    
    def resume(self):
        self.running = True



















