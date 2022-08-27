
from threading import Lock
import os

from Utility.Core import TORRENT, LINK_TYPE, PRIORITY, STATUS
from Utility.TFX import create_peer_data, create_trackers_data

from .Base import Option, Metadata

# Torrent inherited Task Base Classed and special classed


class TrackersInfo:

    def __init__(self, ):
        self.trackers = {}

        self.tracker_stat = {
            TORRENT.TRACKER.STATS.DHT : TORRENT.TRACKER_STATE.NOT_WORKING,
            TORRENT.TRACKER.STATS.LSD : TORRENT.TRACKER_STATE.NOT_WORKING,
            TORRENT.TRACKER.STATS.PEX : TORRENT.TRACKER_STATE.NOT_WORKING
        }

    
    def update_trackers(self, trackers):
        new_trackers = create_trackers_data(trackers)
        self.trackers.update(new_trackers)
    
    def set_stat(self, method, state):
        self.tracker_stat[method] = state

    def set_tracker_state(self, url, state):

        tracker = self.trackers.get(url, False)
        
        if tracker:

            if  state == TORRENT.TRACKER_STATE.NOT_WORKING and \
                tracker[TORRENT.TRACKER.STATE] == TORRENT.TRACKER_STATE.NO_CONNECTION:
                pass
            else:
                tracker[TORRENT.TRACKER.STATE] = state


    def get_trackers(self):
        return self.trackers
    
    def get_stats(self):
        return self.tracker_stat



class PeersInfo:

    def __init__(self):
        
        self.peers = {}
        self.lock = Lock()
        
    
    def update_peers(self, peers):

        new_peers = create_peer_data(peers)        

        self.lock.acquire(True)

        old_keys = list(self.peers.keys())
        new_keys = list(new_peers.keys())
        
        for key in old_keys:
            if key not in new_keys:
                self.peers.pop(key)
        
        self.peers.update(new_peers)

        self.lock.release()

        

    def get_peers(self):
        self.lock.acquire()
        item = self.peers.copy()
        self.lock.release()

        return item
    
    def reset_peers(self):
        self.peers.clear()



class StatusInfo:

    def __init__(self):

        self.status = STATUS.PAUSED
        self.up_speed = 0
        self.down_speed = 0
        self.uploaded = 0
        self.downloaded = 0
        self.progress = 0.0
        self.total_size = 0
        self.eta = -1
        self.share_ratio = 0.0
        self.total_peers = 0
        self.total_seeds = 0
        self.seeders = 0
        self.leechers = 0
        self.seeding_time = 0
        self.active_time = 0
        self.pieces = 0
        self.availability = 0

        self.total_pieces = 0
        self.piece_size = 0
    
    def update_info(self, data):

        for info in data:

            if hasattr(self, info):
                setattr(self, info, data[info])
    
    def set_total_pieces(self, count):
        self.total_pieces = count
    
    def set_piece_size(self, size):
        self.piece_size = size
    
    def set_status(self, state):
        self.status = state
    
    def set_size(self, size):
        self.total_size = size
        


class DetailInfo:

    def __init__(self):
        self._hash = ""
        self.name = ""
        self.save_path = ""
        self.file_count = 0
        self.file_size = 0
        self.up_limit = 0
        self.down_limit = 0
        self.date_completed = ''
        self.date_added = ''
        self.torrent_date = ''
        self.last_seen = ''
        self.comment = ''
    
    def _update_data(self, data):

        for key in data:
            if hasattr(self, key):
                setattr(self, key, data[key])
    
    def set_name(self, name):
        self.name = name
    
    def set_hash(self, _hash):
        self._hash = _hash
    
    def set_save_path(self, new_path):
        self.save_path = new_path
    
    def get_name(self):
        return self.name
    
    def get_hash(self):
        return self._hash
    
    def get_save_path(self):
        return self.save_path
    
    def set_up_limit(self, new_value):
        self.up_limit = new_value

    def set_down_limit(self, new_value):
        self.down_limit = new_value

    def get_up_limit(self):
        return self.up_limit

    def get_down_limit(self):
        return self.down_limit
    
    def set_file_count(self, count):
        self.file_count = count
    
    def set_file_size(self, size):
        self.file_size = size

    def get_file_count(self):
        return self.file_count
    
    def get_file_size(self):
        return self.file_size



class Setting:

    def __init__(self):
        self.options = {x : False for x in TORRENT.OPTIONS.TEXTS}
        self.up_limit = -1
        self.down_limit = -1
    

    def set_up_limit(self, value):
        self.up_limit = value

    def get_up_limit(self):
        return self.up_limit
    
    def set_down_limit(self, value):
        self.down_limit = value

    def get_down_limit(self):
        return self.down_limit
    
    def get_options(self):
        return self.options
    
    def set_option(self, option, state):
        
        if self.options.get(option) != None:
            self.options[option] = state


    def _get_save_data(self):
        return self.options
    
    def _set_save_data(self, data):
        if data:
            for key, value in data.items():
                if self.options.get(int(key)) != None:
                    self.options[int(key)] = value



class FileInfo:
    def __init__(self):

        self.main_folder = None
        self.files = []

        self.single_file = False
        self.size = 0
        self.count = 0
    

    def set_main_folder(self, folder):
        if folder:
            self.main_folder = folder
    
    
    def add_files(self, files):
        if files:
            try:
                self.files.extend(files)

            except Exception as e:
                print(e)
        
            self.__recheck()
    

    def is_single_file(self):
        return self.single_file


    def get_size(self):
        return self.size
    
    def get_count(self):
        return self.count
    
    def get_total_count(self):
        return len(self.files)

    def get_priorities(self):
        return [x.get_priority() for x in self.files]


    def set_priorities(self, priorities):
        for index, file in enumerate(self.files):
            file.set_priority(priorities[index])

        self.update_status()


    def set_progress(self, progress):
        size = 0


        if self.files:
            
            for index, downloaded in enumerate(progress):
                file = self.files[index]

                if file.get_priority():
                    file.set_downloaded(downloaded)
                    size += downloaded
        


        return size            


    def __recheck(self):
        self.single_file = not self.main_folder and len(self.files) == 1


    def update_status(self):

        if not self.files and not self.main_folder:
            return

        if self.single_file:
            self.count = 1
            self.size = self.files[0].get_size()
        else:
            self.count, self.size = self.main_folder.get_selected_stats()

    def has_files(self):
        return len(self.files) > 0



class TorrentOption(Option):

    def __init__(self, _id):
        super().__init__(_id, LINK_TYPE.MAGNET)

        self.file_info = None

        self.sequential = False
        self.up_limit = None

        self.trackers = False
        self.setting = {}



class TorrentMetadata(Metadata):

    def __init__(self, _id):
        super().__init__(_id)

        self._type = LINK_TYPE.MAGNET
        
        self.file_info = None
        self.trackers = None

    def is_successful(self):
        return self.file_info != None

    def __str__(self):
        return f'{self._id} -- {bool(self.main_folder or self.files)}'


class TorrentOptions:
    port = 6881
    listen_interface = '0.0.0.0'
    outgoing_interface = ''
    max_download_rate = -1
    max_upload_rate = 2**20
    save_path = ""
    temp_path = ""
    proxy_host = ''

