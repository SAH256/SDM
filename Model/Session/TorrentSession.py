import os

from PyQt5.QtCore import pyqtSignal, QThread, QTimer
import libtorrent as lt

from Model.Workers.Session.Torrent import TorrentAlertWorker

from Utility.Core import ACTIONS, TORRENT, SDM
from Utility.Structure.Task.Base import ActionRequest
from Utility.Structure.Task.Torrent import TorrentMetadata, FileInfo, TorrentOptions

from Utility.TFX import get_hash, setup_metadata, save_metadata, create_param, reset_param_flags
from Utility.Util import file_ops

from .BaseSession import BaseSession


class Session(BaseSession):

    task_requested = pyqtSignal(ActionRequest)
    metadata_received = pyqtSignal(list)

    def __init__(self, setting):
        super().__init__()

        # create two session 
        # 1- for downloading
        # 2- for handling metadata requests

        self.main_session = lt.session(setting)
        self.test_session = lt.session(setting)
        self.test_session.resume()

        self.__pending = {}

        self.__setup_timer()


    # send all UI requests to session worker handler slot
    def _task_request_handler(self, request):
        self.task_requested.emit(request)


    def add_task(self, task, data = None):
        
        options = TorrentOptions()
        options.save_path = task.get_save_path()
        options.temp_path = os.path.join(SDM.PATHS.TEMP_PATH, task.get_id())

        param = self.__create_param(task.get_id(), options)

        if param:
            super().add_task(task)

            if not param.file_priorities:
                param.file_priorities = task.get_priorities()

            self.main_session.async_add_torrent(param)

    
    def is_paused(self):
        return self.session.is_paused()
    
    def pause(self):
        self.main_session.pause()
        super().pause()

    
    def resume(self):

        self.main_session.resume()

        if not self.running:            
            self.start_worker()
        
        super().resume()


    def __set_running(self, state):
        self.running = state


    # creating timer for metadata requests alert
    def __setup_timer(self):
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.__check_alerts)
        self.timer.start(500)


    def get_metadata(self, _id, param):
        handle = self.test_session.add_torrent(param)

        # if isn't torrent_file
        if not param.ti:
            link = lt.make_magnet_uri(handle)
            save_path = os.path.join(SDM.PATHS.STASH_PATH, f'{_id}.txt')
            file_ops(save_path, link, False, False)

        self.__pending[_id] = param, handle

    
    # metadata alert handler
    def __check_alerts(self):
        for alert in self.test_session.pop_alerts():

            if isinstance(alert, lt.add_torrent_alert):
                if alert.handle.status().has_metadata:
                    self.__manage_metadata(alert.handle)

            elif isinstance(alert, lt.metadata_received_alert):
                self.__manage_metadata(alert.handle)


    def __manage_metadata(self, handle):

        _id = get_hash(handle)
        data = self.__pending.get(_id)

        if data:
            param = data[0]
            status = handle.status()
            tf = handle.torrent_file()

            metadata = setup_metadata(status.name, tf)

            save_metadata(tf, SDM.PATHS.STASH_PATH, _id)
            self.__send_metadata(_id, status.name, metadata)


    


    def __send_metadata(self, _id, name, metadata):
        info = FileInfo()
        info.set_main_folder(metadata[0])
        info.add_files(metadata[1])
        info.update_status()
        
        metadata_obj = TorrentMetadata(_id)
        metadata_obj.file_info = info
        metadata_obj.name = name
        metadata_obj.size = info.get_size()


        self.metadata_received.emit([_id, metadata_obj, True])



    # create param for session
    def __create_param(self, _id, options):
        param = None
        metadata_name = f'{_id}{TORRENT.TORRENT_EXT}'
        link_name = f'{_id}.txt'

        # THESE ARE SEARCHING PATHS FOR METADATA OR MAGNET_TEXT_FILE
        other_paths = [
            os.path.join(SDM.PATHS.TEMP_PATH, _id, metadata_name),
            os.path.join(SDM.PATHS.STASH_PATH, metadata_name),
            os.path.join(SDM.PATHS.STASH_PATH, link_name),
        ]

        try:
            data = self.__pending.get(_id, None)

            if data:
                param = data[0]
                param.save_path = options.save_path
                param.file_priorities = []
            
            else:

                for path in other_paths:
                    if os.path.exists(path):
                        data = path

                        if path.endswith('.txt'):
                            data = file_ops(path, binary = False)

                        _hash, param = create_param(data, options, False)

                        break

            if param:
                reset_param_flags(param)
                self.remove_param(_id)

        except Exception as e:
            print(e)

        return param
            
    

    def remove_param(self, _id):
        items = self.__pending.pop(_id, None)

        if items:
            self.test_session.remove_torrent(items[1])




    def start_worker(self):
        self.__set_running(True)

        self.thread = QThread()
        self.worker = TorrentAlertWorker(self.main_session, self.tasks)

        self.task_requested.connect(self.worker.request_center)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.start_manager)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.checking)

        self.thread.start()
    
    def checking(self):
        self.__set_running(False)
        

    def __get_task(self, _id):
        return self.tasks.get(_id)

