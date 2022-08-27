import os, time
from threading import Lock

from PyQt5.QtWidgets import QApplication
import libtorrent as lt

from Utility.TFX import save_metadata, setup_metadata, save_resume_data, get_hash
from Utility.Core import SDM, TORRENT, STATUS, ACTIONS, STATES
from Utility.Calcs import format_remain_time, format_timestamp
from Utility.Util import sizeChanger

from ..Base import BaseWorker



# Torrent Alert worker for thread
class TorrentAlertWorker(BaseWorker):

    HANDLE_INDEX = 0
    STATUS_INDEX = 1

    def __init__(self, session, tasks):
        super().__init__()
        self.session = session

        self.lock = Lock()

        self.torrents = {}
        self.tasks = tasks

        # alert and handler dict for easy assigning
        # some of them is empty, maybe become in use in future
        self.alert_handlers = {

            lt.add_torrent_alert :              self.add_torrent_handler,
            lt.metadata_received_alert :        self.metadata_received_handler,
            lt.metadata_failed_alert :          self.metadata_failed_handler,
            lt.torrent_checked_alert :          None,
            lt.torrent_paused_alert :           self.pause_handler,
            lt.torrent_resumed_alert :          self.resume_handler,
            lt.torrent_finished_alert :         self.finish_handler,
            lt.torrent_removed_alert :          self.remove_handler,
            lt.torrent_deleted_alert :          None,
            lt.torrent_delete_failed_alert :    None,
            lt.tracker_announce_alert :         self.tracker_state_handler,
            lt.tracker_reply_alert :            self.tracker_state_handler,
            lt.tracker_error_alert :            self.tracker_state_handler,
            lt.file_renamed_alert :             None,
            lt.file_rename_failed_alert :       None,
            lt.file_error_alert :               None,
            lt.file_completed_alert :           None,
            lt.file_prio_alert :                self.priority_handler,
            lt.state_update_alert :             self.state_update_handler,
            lt.state_changed_alert :            self.state_changed_handler,
            lt.save_resume_data_alert :         self.save_resume_handler,
            lt.save_resume_data_failed_alert :  None
        }
    

    # start point of worker for handling alerts and updating
    def start_manager(self):

        while not self.session.is_paused():
            
            self.task_info_center()
            self.alert_center(self.session.pop_alerts())
            self.session.post_torrent_updates()

            time.sleep(0.2)

        else:
            self.task_info_center()
            self.alert_center(self.session.pop_alerts())

        self.finished.emit()

    # UI requests that sent to session is handling here
    def request_center(self, request):

        action = request.get_action()
        items = self.torrents.get(request.get_id())

        if items:

            if action == ACTIONS.PAUSE:
                items[self.HANDLE_INDEX].pause()

            elif action == ACTIONS.RESUME:
                items[self.HANDLE_INDEX].resume()

            elif action == ACTIONS.REMOVE:
                self.session.remove_torrent(items[self.HANDLE_INDEX])

            elif action == ACTIONS.PRIORITY:
                items[self.HANDLE_INDEX].prioritize_files(request.data)

            elif action == ACTIONS.FORCE_REANNOUNCE:
                items[self.HANDLE_INDEX].force_reannounce()

            elif action == ACTIONS.FORCE_RECHECK:
                items[self.HANDLE_INDEX].force_recheck()
            
            elif action == ACTIONS.SAVE_TORRENT:
                self.__save_metadata(request.get_id(), request.data)
            
            elif action == ACTIONS.COPY_LINK:
                self.__copy_magnet_link(request.get_id())
            
            elif action == ACTIONS.SETTING:
                self.__apply_setting(request.get_id())


    # find handler of alert and call it
    def alert_center(self, alerts):
        
        for alert in alerts:
                    
            handler = self.alert_handlers.get(type(alert))

            if handler:
                handler(alert)


    # update torrents data
    def task_info_center(self):

        for _id, items in self.torrents.items():
            task = self.__get_task(_id)
            handle = items[self.HANDLE_INDEX]
            status = items[self.STATUS_INDEX]

            if task:
                if not handle.is_valid():
                    continue

                self.__update_status(_id, handle.status())

                if not task.is_paused() and status.state != lt.torrent_status.seeding:
                    self.task_progress(task, status)
                    self.task_files_progress(task, handle)
                    self.peer_info_handler(task, handle)

                if handle.need_save_resume_data():
                    handle.save_resume_data()


    def task_progress(self, task, status):
        info = self.__create_status_data(status)
        task.update_status(info)


    def task_files_progress(self, task, handle):
        task.set_files_progress(handle.file_progress())


    def peer_info_handler(self, task, handle):
        task.peer_info.update_peers(handle.get_peer_info())


    # FROM THIS SECTION ALERTS START WITH THEIR HELPING FUNCTIONS

    def add_torrent_handler(self, alert):
        handle = alert.handle
        self.__add_torrent(handle)


    def state_update_handler(self, alert):

        for status in alert.status:
            _id = get_hash(status.handle)
            items = self.torrents.get(_id, False)
            
            if items:
                items[self.STATUS_INDEX] = status
                self.__update_status(_id, status)
                

    def metadata_received_handler(self, alert):
    
        _id = get_hash(alert.handle)

        task = self.__get_task(_id)
        
        if task:
            self.__manage_metadata(task, alert.handle)
            
        self.__update_status(_id, alert.handle.status())

    
    def metadata_failed_handler(self, alert):
        _id = get_hash(alert.handle)
        
        task = self.__get_task(_id)
        print('metadata Failed')

        if task:
            task.metadata_fail(alert.error.message())


    def pause_handler(self, alert):        
        _id = get_hash(alert.handle)
        task = self.__get_task(_id)
        alert.handle.save_resume_data()

        if task:
            task.status_info.set_status(STATUS.PAUSED)
            self.__update_status(_id, alert.handle.status())
            self.__change_tracker_stats(_id)


    def resume_handler(self, alert):
        _id = get_hash(alert.handle)
        status = alert.handle.status()

        self.__update_status(_id, status)


    def tracker_state_handler(self, alert):

        state = TORRENT.TRACKER_STATE.NOT_WORKING

        if isinstance(alert, lt.tracker_reply_alert):
            state = TORRENT.TRACKER_STATE.WORKING
        elif isinstance(alert, lt.tracker_announce_alert):
            state = TORRENT.TRACKER_STATE.UPDATING
        
        _id = get_hash(alert.handle)
        task = self.__get_task(_id)

        if task:
            task.tracker_info.set_tracker_state(alert.url, state)
            self.__change_tracker_stats(_id, task.is_paused())


    def save_resume_handler(self, alert):
        _id = get_hash(alert.handle)
        task = self.__get_task(_id)

        if task:
            save_path = os.path.join(SDM.PATHS.TEMP_PATH, _id)
            save_path = os.path.join(save_path, _id + TORRENT.FASTRESUME_EXT)
            save_resume_data(save_path, alert.params)


    # may need to fill it in future...
    def state_changed_handler(self, alert):
        pass


    def remove_handler(self, alert):
        _id = get_hash(alert.info_hashes)
        self.__remove_torrent(_id)


    def finish_handler(self, alert):
        _id = get_hash(alert.handle)
        task = self.tasks.get(_id)

        if task:
            status = alert.handle.status()
            task.set_state(STATES.COMPLETED)

            self.task_progress(task, status)
            self.__update_status(_id, status)


    def priority_handler(self, alert):

        _id = get_hash(alert.handle)
        task = self.__get_task(_id)

        alert.handle.save_resume_data()
        self.__update_detail(alert.handle)

        self.task_progress(task, alert.handle.status())


    def __update_detail(self, handle):
        _id = get_hash(handle)
        task = self.__get_task(_id)

        if task:
            detail = self.__create_detail_data(handle.status())
            task.update_details(detail)


    def __add_torrent(self, handle):
        _id = get_hash(handle)
        status = handle.status()

        task = self.__get_task(_id)

        if task:

            task.set_name(status.name)
            task.set_trackers(handle.trackers())

            self.__update_detail(handle)

            self.__add_handle(_id, handle)
            self.__apply_setting(task.get_id())
            
            if status.has_metadata:
                self.__manage_metadata(task, handle)

            if task.is_paused():
                handle.pause()
            else:
                handle.resume()



    def __manage_metadata(self, task, handle):
    
        status = handle.status()
        tf = handle.torrent_file()

        detail = self.__create_detail_data(status)
        task.update_details(detail)

        task.status_info.set_total_pieces(tf.num_pieces())
        task.status_info.set_piece_size(tf.piece_length())

        if not task.has_metadata():
            priorities = handle.get_file_priorities()
            main_folder, files = setup_metadata(task.get_name(), tf, priorities)

            task._set_metadata(main_folder, files)

        self.__save_metadata(task.get_id())
    

    def __apply_setting(self, _id):
        task = self.__get_task(_id)
        items = self.torrents.get(_id)
        
        if task:
            handle = items[self.HANDLE_INDEX]
            setting = task.get_setting()

            handle.set_download_limit(setting.get_down_limit())
            handle.set_upload_limit(setting.get_up_limit())

            for flag, state in setting.get_options().items():
                if state:
                    handle.set_flags(flag)
                else:
                    handle.unset_flags(flag)

            self.__change_tracker_stats(_id, task.is_paused())


    def __save_metadata(self, _id, save_path = None):
        items = self.torrents.get(_id)

        if not save_path:
            save_path = os.path.join(SDM.PATHS.TEMP_PATH, _id)

        torrent_file = items[self.HANDLE_INDEX].torrent_file()

        save_metadata(torrent_file, save_path, _id)


    def __copy_magnet_link(self, _id):
        items = self.torrents.get(_id)

        if items:
            link = lt.make_magnet_uri(items[self.HANDLE_INDEX])
            QApplication.clipboard().setText(link)


    def __change_tracker_stats(self, _id, paused = True):
        nw = TORRENT.TRACKER_STATE.NOT_WORKING
        dis = TORRENT.TRACKER_STATE.DISABLED
        wk = TORRENT.TRACKER_STATE.WORKING
            
        dht = TORRENT.TRACKER.STATS.DHT
        lsd = TORRENT.TRACKER.STATS.LSD
        pex = TORRENT.TRACKER.STATS.PEX
        

        task = self.__get_task(_id)
        items = self.torrents.get(_id)

        if task and items:
            tracker = task.tracker_info
            f = items[self.HANDLE_INDEX].flags()

            temp = {
                dht : (dis if (f & lt.torrent_flags.disable_dht) else wk) if not paused else nw,
                lsd : (dis if (f & lt.torrent_flags.disable_lsd) else wk) if not paused else nw,
                pex : (dis if (f & lt.torrent_flags.disable_pex) else wk) if not paused else nw,
            }


            for method, state in temp.items():
                tracker.set_stat(method, state)


    def __get_task(self, key):
        self.lock.acquire()
        task = self.tasks.get(key, False)
        self.lock.release()
        
        return task
        
    
    def __add_handle(self, _id, handle):
        self.lock.acquire()
        self.torrents[_id] = [handle, handle.status()]
        self.lock.release()

    def __remove_torrent(self, _id):
        self.lock.acquire()

        self.tasks.pop(_id, None)
        self.torrents.pop(_id, None)

        self.lock.release()


    def __update_status(self, _id, status):
        task = self.__get_task(_id)

        if task:

            s = STATUS.PAUSED

            if task.is_completed():
                s = STATUS.COMPLETED
            else:
                if not task.is_paused():
                    s = STATUS.TORRENT_ORDER[status.state]
            
            task.set_status(s)


    def __create_status_data(self, status):
        down_sp = status.download_payload_rate
        eta = -1
        
        down = status.all_time_download
        up = status.all_time_upload
        ratio = down / (up if up else 1)

        if down_sp:
            eta = (status.total_wanted - down) / down_sp
            eta = round(eta) + 1


        temp_info = {
            TORRENT.STATUS.STATUS           : STATUS.TORRENT_ORDER[status.state],
            TORRENT.STATUS.UPLOAD_SPEED     : status.upload_payload_rate,
            TORRENT.STATUS.DOWNLOAD_SPEED   : status.download_payload_rate,
            TORRENT.STATUS.UPLOADED         : up,
            TORRENT.STATUS.DOWNLOADED       : status.total_wanted_done,
            TORRENT.STATUS.PROGRESS         : round(status.progress, 4),
            TORRENT.STATUS.ETA              : eta,
            TORRENT.STATUS.SHARE_RATIO      : round(ratio, 3),
            TORRENT.STATUS.TOTAL_PEERS      : status.list_peers,
            TORRENT.STATUS.TOTAL_SEEDS      : status.list_seeds,
            TORRENT.STATUS.SEEDERS          : status.num_seeds,
            TORRENT.STATUS.LEECHERS         : status.num_peers - status.num_seeds,
            TORRENT.STATUS.SEEDING_TIME     : status.seeding_time,
            TORRENT.STATUS.ACTIVE_TIME      : status.active_time,
            TORRENT.STATUS.PIECES           : status.num_pieces,
            TORRENT.STATUS.AVAILABILITY     : round(status.distributed_copies, 6)
        }

        return temp_info
    
    def __create_detail_data(self, status):
        temp_detail = {
            TORRENT.DETAIL.HASH : status.info_hash.to_bytes().hex().upper(),
            TORRENT.DETAIL.NAME : status.name,
            TORRENT.DETAIL.SAVE_PATH : status.save_path,
            TORRENT.DETAIL.FILE_SIZE : status.total_wanted,
            TORRENT.DETAIL.UPLOAD_LIMIT : status.handle.upload_limit(),
            TORRENT.DETAIL.DOWN_LIMIT : status.handle.download_limit(),
            TORRENT.DETAIL.DATE_COMPLETED : format_timestamp(status.completed_time),
            TORRENT.DETAIL.DATE_ADDED : format_timestamp(status.added_time),
            TORRENT.DETAIL.TORRENT_DATE : format_timestamp(status.torrent_file.creation_date()),
            TORRENT.DETAIL.LAST_SEEN : format_timestamp(status.last_seen_complete),
            TORRENT.DETAIL.COMMENT : status.torrent_file.comment()
        }
        
        return temp_detail


