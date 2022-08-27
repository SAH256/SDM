from PyQt5.QtCore import QObject, pyqtSignal

from Utility.Structure.Task.Base import ActionRequest
from Utility.Core import QUEUE, ACTIONS, SAVES

from .Queue import Queue


# Queue manager class for basic operation on queues : create, add, remove, request
class QueueManager(QObject):
    
    requested = pyqtSignal(ActionRequest)

    def __init__(self):
        super().__init__()

        self.__system_request = None
            
        self.queues = {}

        
    def create_queue(self, name, timer_type = QUEUE.SETTING.ONE_TIME, creator_type = QUEUE.SETTING.SYSTEM_TYPE):
        q = Queue(name, timer_type, creator_type)
        q.action_requested.connect(self.__request_handler)
        self.queues[name] = q

        return q

    def remove_queue(self, name):

        q = self.queues.pop(name)

        if q:
            q.reset()

    def get_queue_names(self):
        return list(self.queues.keys())
        
    def get_info(self):
        return [(name, q.get_timer_type() == QUEUE.SETTING.ONE_TIME, q.get_creator_type() == QUEUE.SETTING.SYSTEM_TYPE) 
                for name, q in self.queues.items()]

    def get_state(self):
        return [(name, q.is_running()) for name, q in self.queues.items()]
    

    def is_running(self):
        state = False

        for queue in self.queues.values():
            if queue.is_running():
                state = True
                break
        
        return state


    def get_queues(self):
        return self.queues

    def get_queue(self, name):
        return self.queues.get(name)

    def add_task(self, queue, task):
        q = self.queues.get(queue)

        if q:
            q.add_task(task)

    # change tasks queue
    def change_queue(self, source, dest, items):
            
        queue = self.queues.get(source)
        if queue:
            items = queue.remove_tasks(items)
            
        queue = self.queues.get(dest)
        if queue:
            for task in items:
                queue.add_task(task)


    def remove_task(self, task):
        queue = self.queues.get(task.get_queue())
        if queue:
            if queue.has_task(task):
                queue.remove_task(task)


    # mergin to queue request by precedence
    def __merge_requests(self, req1, req2):
        result = [False] * 3

        opt = QUEUE.PROCESS.POST.OPTIONS

        for i in range(len(result)):

            # second option of request is about turn off method (shut_down, sleep, hiber)
            # so we must make sure the one with higher precedence selected
            # shutdown < sleep < hibernate
            if i == 1:
                if req1[i] and req2[i]:
                    result[i] = req1[i] if ( opt.index(req1[i]) < opt.index(req2[i]) ) else req2[i]  # if req1 option is superior to req2 then select it (shutdown will preferred to sleep and sleep preferred to hibernate)
                elif req1[i]:
                    result[i] = req1[i]
                elif req2[i]:
                    result[i] = req2[i]
                    
            else:
                result[i] = bool(req1[i] + req2[i])
            
        return result


    def __request_handler(self, request):

        if request.get_action() != ACTIONS.SYSTEM:
            self.requested.emit(request)
        else:
            self.__check_request(request)


    # check if any request is on the line or not,
    # if it is then merge both of them
    def __check_request(self, request):
        
        if self.__system_request:
            data = self.__merge_requests(self.__system_request.data, request.data)
        else:
            self.__system_request = request
        
        if not self.is_running():
            self.requested.emit(self.__system_request)


    def _get_save_data(self):
        data = {}

        for name, queue in self.queues.items():
            temp_data = queue._get_save_info()

            data[name] = {
                SAVES.SLOTS.PARAM : temp_data[0],
                SAVES.SLOTS.TIMER : temp_data[1],
                SAVES.SLOTS.FILES : temp_data[2],
                SAVES.SLOTS.PROCESS : temp_data[3],
                SAVES.SLOTS.SETTING : temp_data[4],
            }

        return data


