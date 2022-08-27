from PyQt5.QtCore import pyqtSignal

from Utility.Structure.Task.Torrent import PeersInfo, TrackersInfo, StatusInfo, DetailInfo, FileInfo, Setting
from Utility.Structure.Task.Torrent import TorrentOption, TorrentMetadata

from Utility.Core import LINK_TYPE, ACTIONS, TORRENT, ERRORS, SAVES

from .Base import BaseTask


class TorrentTask(BaseTask):

    metadata_responded = pyqtSignal(list)

    def __init__(self, _id):
        super().__init__(_id)

        self.set_type(LINK_TYPE.MAGNET)

        self.status_info = StatusInfo()
        self.detail_info = DetailInfo()
        self.file_info = FileInfo()
        self.tracker_info = TrackersInfo()
        self.peer_info = PeersInfo()
        self.setting = Setting()



    def setup(self, options):
        super().setup(options)

        self.setting.set_up_limit(options.up_limit)
        self.setting.set_down_limit(options.down_limit)
        file_info = options.file_info

        # if torrent option has metadata file info then use it
        if file_info:
            self.file_info = file_info
            self.set_metadata(True)

        self.set_size(self.file_info.get_size())
        self.detail_info.set_file_count(self.file_info.get_count())

        self.setting.set_option(TORRENT.OPTIONS.SEQUENTIAL, options.sequential)
        
        if options.setting:
            self.setting._set_save_data(options.setting)


    def get_up_limit(self):
        return self.setting.get_up_limit()
    
    def get_down_limit(self):
        return self.setting.get_down_limit()


    def set_size(self, size):
        super().set_size(size)
        self.detail_info.set_file_size(size)
        self.status_info.set_size(size)


    def _set_metadata(self, main_folder, files):
        
        self.file_info.set_main_folder(main_folder)
        self.file_info.add_files(files)

        self.file_info.update_status()

        size = self.file_info.get_size()
        count = self.file_info.get_count()

        self.set_size(size)
        self.detail_info.set_file_count(count)
        

    def metadata_failed(self, error_msg):
        print(error_msg)

    def has_metadata(self):
        return self.file_info.has_files()

    def update_status(self, data):
        self.status_info.update_info(data)

        self.set_down_speed(self.status_info.down_speed)
        self.set_up_speed(self.status_info.up_speed)
        self.set_size(self.status_info.total_size)

        self.set_eta(self.status_info.eta)
        self.set_progress(self.status_info.progress)


    def update_details(self, details):

        self.detail_info._update_data(details)
        self.detail_info.set_file_count(self.file_info.get_count())
        
        self.status_info.total_size = self.file_info.get_size()


    def set_files_progress(self, progress):
        s = self.file_info.set_progress(progress)
        self.set_downloaded(s)


    def set_trackers(self, trackers):
        self.tracker_info.update_trackers(trackers)
        
    
    def is_single_file(self):
        return self.file_info.is_single_file()

    def get_details(self):
        return self.detail_info
    
    def get_status(self):
        return self.status_info

    def get_trackers(self):
        return self.tracker_info.get_trackers()

    def get_peers(self):
        return self.peer_info.get_peers()

    def get_setting(self):
        return self.setting

    def set_up_speed(self, speed):
        self.info.upload_speed = speed
    
    def get_priorities(self):
        return self.file_info.get_priorities()
    
    def set_priorities(self, priorities):
        self.file_info.set_priorities(priorities)
    

    def send_request(self, request):
        if request.get_action() == ACTIONS.PRIORITY:
            request.data = self.get_priorities()
        
        self.action_requested.emit(request)

    def _get_data(self):
        return [
            self.status_info,
            self.detail_info,
            self.file_info,
            self.tracker_info,
            self.peer_info,
            self.setting
        ]


    def _get_save_data(self):
        data = super()._get_save_data()

        data[SAVES.SLOTS.TYPE] = self.get_type()

        data[SAVES.SLOTS.SEQUENTIAL] = True
        data[SAVES.SLOTS.UP_LIMIT] = self.get_up_limit()
        data[SAVES.SLOTS.SETTING] = self.setting._get_save_data()

        return data


    # delete file info data [for safety of delete on other refrences]
    def __del__(self):
        self.file_info.files.clear()
        if self.file_info.main_folder:
            del self.file_info.main_folder