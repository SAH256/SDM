from datetime import datetime as dt
import os

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from Utility.Structure.Task.Base import Request
from Utility.Structure.Task.Torrent import TorrentOption
from Utility.Structure.Task.Http import MultiRequest, HttpOption

from Utility.Gui import findCategory
from Utility.Actions import remove_dir, remove_file
from Utility.TFX import create_param, reset_param_flags
from Utility.Util import create_id, split_file_name, get_default_part
from Utility.Core import HTTP, SDM, TORRENT, LINK_TYPE, QUEUE, CATEGORY, ACTIONS, SETTING, DUPLICATE, ERRORS, STATES, SAVES


from .Workers.Head.Single import SingleWorker
from .Workers.Head.Multi import MultiWorker

from .Task.Http import HttpTask
from .Session.HttpSession import HttpSession

from .Task.Torrent import TorrentTask
from .Session.TorrentSession import Session

from .Schedule.Manager import QueueManager

from .Saveable import Saveable


class Client(Saveable, QtCore.QObject):

    requested = QtCore.pyqtSignal(list)
    
    def __init__(self, setting):
        super().__init__()

        self.setting = setting

        self.threads = {}
        self.slots = {}
        self.tasks = {}
        self.pending_tasks = {}
        self.garbage = []
        self.threads_garbage = []

        self.queue_manager = QueueManager()
        self.queue_manager.requested.connect(self._request_handler)


        self.fetch_methods = {
            LINK_TYPE.HTTP : self.__http_head,
            LINK_TYPE.MAGNET : self.__torrent_head
        }

        self.sessions = {
            LINK_TYPE.HTTP: self.__http_session(),
            LINK_TYPE.MAGNET : self.__create_torrent_session()
        }

        self.__create_queues()
        self.__setup_timer()
    

    # creat app default queues
    def __create_queues(self):
        queues = [
            ('Main Download Queue', QUEUE.SETTING.ONE_TIME),
            ('Synchronization Queue', QUEUE.SETTING.PERIODIC),
        ]

        for item in queues:
            self.queue_manager.create_queue(*item)


    # make timer for cleaning and saving funcions
    def __setup_timer(self):
        slots = [
            self.__remove_garbages,
            self.__check_completed,
            self.save_state
        ]

        self.__timer = QtCore.QTimer()
        self.__timer.setSingleShot(False)

        [self.__timer.timeout.connect(slot) for slot in slots]
        self.__timer.start(2000)


    # fetch metadata of link
    def fetch_metadata(self, req, slot):
        handler = self.fetch_methods.get(req._type)

        if handler:
            handler(req, slot)


    def add_task(self, options, add = True, start = False, duplicate_option = None):
        
        task = None
        info = None

        if add:
            task = self.__setup_pending(options, duplicate_option)
        else:
            self.__remove_pending(options)

        if task:
            if not task.is_completed():
                self.queue_manager.add_task(task.get_queue(), task)
            
            if start:
                task.resume()

            info = task.get_info()
            
        return info


    def fetch_multi(self, request, slot):    
        self.slots[request.get_id()] = slot
        self.__start_http_head(request, False)



    def get_queues(self):
        return self.queue_manager.get_queue_names()


    def get_queue_manager(self):
        return self.queue_manager


    def get_task_info(self, _id):
        item = self.get_task(_id)
        
        if item:
            return item.get_info()



    def stop_session(self):
        for ses in self.sessions.values():
            if ses:
                ses.pause()


    def get_task(self, _id):
        task = self.tasks.get(_id)

        if not task:
            task = self.pending_tasks.get(_id)
        
        return task


    # get all torrents info
    def get_torrents_info(self):
        data = {}

        for task in self.tasks.values():
            if task.get_type() == LINK_TYPE.MAGNET:
                data[task.get_info()] = task._get_data()
        
        return data


    def has_duplicate(self, url, _type):
        duplicate = False

        tasks = set(self.tasks.values())
        tasks = tasks.union(set(self.pending_tasks.values()))

        for task in tasks:
            if _type == task.get_type() and url == task.get_url():
                duplicate = True
                break

        return duplicate


    # register http head request's slot and send request
    def __http_head(self, req, slot):

        self.slots[req.get_id()] = slot
        self.__start_http_head(req)


    # create http head request thread
    def __start_http_head(self, req, is_single = True):

        if is_single:
            worker = SingleWorker(req)
        else:
            worker = MultiWorker(req)

        thread = QtCore.QThread()

        worker.moveToThread(thread)
        thread.started.connect(worker.run)

        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.finished.connect(self.__release_thread)

        thread.finished.connect(self.__remove_threads_garbage)
        thread.finished.connect(thread.deleteLater)
        
        worker.fetched.connect(self.__response_handler)

        self.threads[req.get_id()] = thread, worker

        thread.start()



    def __release_thread(self, _id):
        self.slots.pop(_id)

        data = self.threads.pop(_id)
        self.threads_garbage.append(data)
    

    def __remove_threads_garbage(self):
        self.threads_garbage.clear()
        

    @QtCore.pyqtSlot(list)
    def __response_handler(self, meta):
        _id = meta[0]
        metadata = meta[1]

        slot = self.slots.get(_id)
        if slot:
            slot(metadata)


    def __create_task(self, _id, _type):

        if _type == LINK_TYPE.HTTP:
            task = HttpTask(_id)
        else:
            task = TorrentTask(_id)
        
        return task



    def __http_session(self):
        ses = HttpSession()
        ses.resume()
        return ses

    def __create_torrent_session(self):

        setting = self.setting.get(SETTING.TORRENT).get_session_setting()

        self.torrent_session = Session(setting)
        self.torrent_session.metadata_received.connect(self.__response_handler)
        self.torrent_session.resume()

        return self.torrent_session


    # create torrent paream object for downloading metadata
    def __create_param(self, url):
        op = self.setting.get(SETTING.TORRENT).get_option()
        op.temp_path = SDM.PATHS.TEMP_PATH

        return create_param(url, op)



    # send torrent metadata request to session
    def __torrent_head(self, req, slot):

        param_items = self.__create_param(req.url)
        error = ERRORS.PARSE_FAILED

        if param_items:
            _hash, param = param_items

            self.slots[_hash] = slot
            req._id = _hash

            self.torrent_session.get_metadata(_hash, param)            
        else:
            slot(error, False)



    # setup pending task that waits for either user permission or metadata
    def __setup_pending(self, options, duplicate_option = None):
        
        task = self.pending_tasks.get(options._id)

        # if user added task without requesting metadata then, create a task right now
        if not task:
            task = self.__create_task(options._id, options._type)
        
        self.__manage_duplication(options, duplicate_option)
        task.setup(options)

        if options.metadata or options._type == LINK_TYPE.MAGNET:
            old_id = options._id

            if options._type == LINK_TYPE.HTTP:
                self.__change_id(options)

            if not task.is_completed():
                self.__add_to_session(task)

            self.pending_tasks.pop(old_id, None)
            self.tasks[task.get_id()] = task

        
        else:
            self.__change_slot(options._id)
            self.pending_tasks[options._id] = task


        return task


    # manage duplicate task based on user choice
    # it is still incomplete and need more works
    def __manage_duplication(self, option, duplicate_option):
        
        if option._type == LINK_TYPE.HTTP and duplicate_option == DUPLICATE.NUMBER:
            option.duplicate_number = self.__duplicate_count(option.url, option._type)
        else:
            if duplicate_option == DUPLICATE.MERGE_TRACKERS:
                'MERGE TRACKERS'


    # change id of metadataless task based on new data
    def __change_id(self, option):
        if option._type == LINK_TYPE.MAGNET:
            return

        old_id = option._id

        url = option.url
        name = option.name
        time_stamp = option.date

        new_id = create_id(url, name, time_stamp)
        option._id = new_id


    # if task added without waiting for metadata then
    # change response's slot to client one
    def __change_slot(self, _id):
        if self.slots.get(_id):
            self.slots[_id] = self.__task_metadata_handler


    def __add_to_session(self, task, data = None):
        ses = self.sessions.get(task.get_type())

        if ses:
            ses.add_task(task, data)
            

    # request handle for tasks' UI option requests
    def _request_handler(self, request):
        _id = request.get_id()
        task = self.get_task(_id)
        action = request.get_action()


        if action == ACTIONS.PAUSE:
            self._pause_task(_id)

        elif action == ACTIONS.RESUME:
            self._resume_task(_id)
        
        elif action == ACTIONS.REMOVE:
            self._remove_task(_id, request.data)
        
        elif action == ACTIONS.OPEN:
            path = task.get_dirname()
            
            if os.path.exists(path):
                os.startfile(path)

        elif action == ACTIONS.FOLDER:
            path = task.get_save_path()
            os.startfile(path)

        elif action == ACTIONS.CHANGE_URL:
            task.set_url(request.data)
        
        elif action == ACTIONS.SYSTEM:
            self.requested.emit(request.data)

        else:

            if action == ACTIONS.COPY_LINK and task.get_type() == LINK_TYPE.HTTP:
                url = task.get_url()
                QApplication.clipboard().setText(url)
            else:
                task.send_request(request)



    def _pause_task(self, _id):
        task = self.get_task(_id)

        if task:
            task.pause()


    def _resume_task(self, _id):
        task = self.get_task(_id)

        if task:
            
            if task.has_metadata() or task.get_type() == LINK_TYPE.MAGNET:
                task.resume()
            else:
                # if task doesn't have metadata then send head request
                self.__send_task_head(task)



    def _pause_all(self):

        for _id, task in self.tasks.items():
            if task.get_state() == STATES.RUNNING:
                self._pause_task(_id)
    

    def _resume_all(self):

        for _id, task in self.tasks.items():
            if task.get_state() == STATES.PAUSED:
                self._resume_task(_id)


    def _remove_all_finished(self, disk = False):

        items_list = list(self.tasks.items())
        result = []

        for _id, task in items_list:
            try:
                if task.get_state() == STATES.COMPLETED:
                    result.append(_id)
                    self._remove_task(_id, disk)
            except:
                pass
        
        return result



    # send task head for metadataless task
    def __send_task_head(self, task):
        _id = create_id(task.get_url(), time_stamp = dt.now().timestamp())

        req = Request(task.get_id(), task.get_url(), task.get_type())
        

        slot = self.__task_metadata_handler

        self.fetch_metadata(req, slot)


    # client method for checking if task is paused for removing or not
    def _remove_task(self, _id, disk = False):

        task = self.tasks.pop(_id, None)

        if not task:
            task = self.pending_tasks.pop(_id, None)

        if task:
            task.pause()
            self.garbage.append((task, disk))
            self.__timer.start(3000)
            

    # private client method for removing tasks by timer
    def __remove_garbages(self):

        for task, from_disk in self.garbage:
            task.remove()
            remove_dir(task.get_temp_path())

            if from_disk and task.has_metadata():
                remove_file(task.get_dirname())

        self.garbage.clear()
    

    # remove completed tasks from its queue
    def __check_completed(self):
        for task in self.tasks.values():
            if task.is_completed():
                self.queue_manager.remove_task(task)
                
                


    # internal task metadata handler for http tasks that added without fetching head
    def __task_metadata_handler(self, response, fetched):

        if fetched:
            # task = self.get_task(response._id)
            task = self.pending_tasks.get(response._id)
            option = self.__create_http_option(response)

            if task:
                self.add_task(option, True, True)

        else:
            task = self.pending_tasks.get(response._id)

            if task:
                task.set_status(HTTP.RESPONSE.ERROR_STATUS.get(response.code))


    # client http response handler
    def __create_http_option(self, response):
        option = HttpOption(response._id)

        option.url = response.url
        option.name = response.name
        option.size = response.size
        option.resume = response.resume
        option.etag = response.etag

        option.metadata = True

        extension = split_file_name(response.name)[-1]

        option.category = findCategory(extension)
        option.path = self.setting.get(SETTING.PATH).get_path(option.category)
        option.part = get_default_part(response.size, response.resume)

        return option
    

    # remove pending tasks
    def __remove_pending(self, options):

        if options._type == LINK_TYPE.MAGNET:
            self.torrent_session.remove_param(options._id)
        else:
            self.pending_tasks.pop(options._id, None)


    # add removed tasks to garbage trash for clearing later
    def __add_to_garbage(self, task, disk = False):
        self.garbage.append((task, disk))


    def __duplicate_count(self, url, _type):
        count = 0

        tasks = set(self.tasks.values())
        tasks = tasks.union(set(self.pending_tasks.values()))

        for task in tasks:
            if _type == task.get_type() and url == task.get_url():
                count += 1
        
        return count


    def __create_option(self, _type):
        option = None

        if _type == LINK_TYPE.HTTP:
            option = HttpOption(-1)
        else:
            option = TorrentOption(-1)
        
        return option


    # saving tasks and queues state to a file
    def save_state(self):

        name = SDM.PATHS.SAVE_DATA_PATH

        save_data = {
            SAVES.TYPES.QUEUE : self.queue_manager._get_save_data(),
            SAVES.TYPES.TASK : self.__save_tasks(),
        }

        self._store_data(name, save_data)



    def __save_tasks(self):
    
        save_data = []
        all_tasks = {**self.tasks, **self.pending_tasks}

        for _id, task in all_tasks.items():
            data = task._get_save_data()
            save_data.append(data)
        
        return save_data
        

    # restore tasks and queues from saved file
    def restore_state(self):
        name = SDM.PATHS.SAVE_DATA_PATH
        data = self._retrieve_data(name)

        if data:
            self.__restore_queue(data.get(SAVES.TYPES.QUEUE))
            self.__restore_tasks(data.get(SAVES.TYPES.TASK))



    def __restore_queue(self, data):

        for name in data:

            queue = self.queue_manager.get_queue(name)

            if not queue:
                queue = self.queue_manager.create_queue(name, *data[name].get(SAVES.SLOTS.PARAM))

            timer = data[name].get(SAVES.SLOTS.TIMER)
            files = data[name].get(SAVES.SLOTS.FILES)
            process = data[name].get(SAVES.SLOTS.PROCESS)
            setting = data[name].get(SAVES.SLOTS.SETTING)

            queue._set_save_data(timer, files, process, setting)


    def __restore_tasks(self, data):

        for entry in data:
            op = self.__create_option(entry[SAVES.SLOTS.TYPE])

            for key in entry:
                if hasattr(op, key):
                    setattr(op, key, entry[key])
            
            self.add_task(op)
        


    # get all tasks info object
    def get_all_info(self):
        all_tasks = {**self.tasks, **self.pending_tasks}

        info_list = [x.get_info() for x in all_tasks.values()]
        info_list.sort(key = lambda x : x.date)

        return info_list







