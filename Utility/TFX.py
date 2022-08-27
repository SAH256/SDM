import libtorrent as lt
import os

from .Structure.Task.Base import File, Folder
from .Core import TORRENT
from .Util import file_ops


# making torrent param object from torrent file or magnet link
def create_param(file_name, options, for_metadata = True):

    magnet_sign = "magnet:"
    torrent_param = None
    hash_obj = None

    if file_name.startswith(magnet_sign):
        torrent_param = lt.parse_magnet_uri(file_name)
        hash_obj = torrent_param.info_hash
    else:
        torrent_param = lt.add_torrent_params()
        torrent_info = lt.torrent_info(file_name)
        hash_obj = torrent_info.info_hash()
        resume_file = os.path.join(options.temp_path, create_hash_name(hash_obj) + TORRENT.FASTRESUME_EXT)

        # if this file has resume data in its temporary directory
        if os.path.join(resume_file):
            try:
                torrent_param = lt.read_resume_data( file_ops(resume_file) )
            except:
                pass

        torrent_param.ti = torrent_info


    if torrent_param:
        _hash = create_hash_name(hash_obj)

        torrent_param.storage_mode = lt.storage_mode_t.storage_mode_sparse

        torrent_param.flags |= lt.torrent_flags.duplicate_is_error 
        torrent_param.flags |= lt.torrent_flags.upload_mode
        torrent_param.flags |= lt.torrent_flags.sequential_download
        
        if for_metadata:
            torrent_param.save_path = options.temp_path
            torrent_param.file_priorities = [0] * 10000000
        else:
            torrent_param.save_path = options.save_path

    return _hash, torrent_param


# reset param flags for adding to main session
def reset_param_flags(param):
    param.flags ^= lt.torrent_flags.upload_mode
    param.flags ^= lt.torrent_flags.auto_managed
    param.flags |= lt.torrent_flags.paused



# get all subfiles of File object
def get_total_files(folder):
    files = folder.get_files()
    
    for f in folder.get_folders():
        temp_files = get_total_files(f)
        files.extend(temp_files)

    return files

# get all subfolders of folder object
def get_total_folders(folder):
    folders = []
    dir_folder = folder.get_folders()

    for f in dir_folder:
        fs = get_total_folders(f)
        folders.extend(fs)
    
    folders.extend(dir_folder)

    return folders


def split_path(path):
    return path.split("\\")[1:-1]    # return anything except root and file_name


# get all files data from torrent file storage
def make_files_list(file_storage, priorities = None):
    files = file_storage.files()

    temp_dirs = []

    for i in range(file_storage.num_files()):
        
        name = files.file_name(i)
        temp_path = split_path( files.file_path(i) )
        size = files.file_size(i)
        prio = 4

        if priorities:
            prio = priorities[i]
        
        temp_file = File(name, None, size, prio, i)


        temp_path.append(temp_file) # add file to end of its directory

        temp_dirs.append(temp_path) # add directory/File to container

    return temp_dirs



# find file and folders and them to parent folder object
def manage_hierarchy(paths, name, parent = None):

    subs = {}
    files = []
    folders = []

    for path in paths:

        if len(path) == 1:
            files.append( path[0] )
            
        else:
            temp_item = path[0]

            container = subs.get(temp_item, False)

            if not container:
                container = []
                subs[temp_item] = container

            container.append( path[1:] )


    folder = Folder(name, parent)

    for item in subs:
        temp_sub = manage_hierarchy(subs[item], item, folder)
        folders.append(temp_sub)

    folder.add_folder(folders)
    folder.add_file(files)

    return folder


# find files relation and main folder
def organize_files(name, directories):

    files = [x[-1] for x in directories]
    main_folder = None

    if len(files) > 1:
        main_folder = manage_hierarchy(directories, name)
    
    return main_folder, files


# creating metadata object representation to Folder and File
def setup_metadata(name, file_storage, priorities = None):

    files_list = make_files_list(file_storage, priorities)
    metadata = organize_files(name, files_list)

    return metadata


# change hash object to hex string
def create_hash_name(hash_obj):
    data = hash_obj.to_bytes()
    return str(data.hex()).upper()


# save torrent metadata to a file
def save_metadata(torrent_file, save_path, name):
    ct = lt.create_torrent(torrent_file)
    te = ct.generate()
    data = lt.bencode(te)

    file_name = os.path.join(save_path, name + TORRENT.TORRENT_EXT)

    file_ops(file_name, data, False)


# save torrent resume data
def save_resume_data(save_path, param):
    buff = lt.write_resume_data_buf(param)
    file_ops(save_path, buff, False)

# get hash string of torrent object in hex
def get_hash(obj):
    _hash = None

    if isinstance(obj, lt.torrent_handle):
        _hash = obj.info_hash()
    else:
        _hash = obj.get_best()

    return _hash.to_bytes().hex().upper()


# extract peer data from list of peer objects
def create_peer_data(peers):
    
    result = {}

    for peer in peers:
        
        client = None
        connected = False

        if (peer.flags & peer.handshake) or (peer.flags & peer.connecting) :
            continue
        else:
        
            client = peer.client.decode()
            connected = True

        temp = {
            TORRENT.PEER.CLIENT : client,
            TORRENT.PEER.TOTAL_DOWN : peer.total_download,
            TORRENT.PEER.TOTAL_UP : peer.total_upload,
            TORRENT.PEER.SPEED_UP : peer.up_speed,
            TORRENT.PEER.SPEED_DOWN : peer.down_speed,
            TORRENT.PEER.DOWN_QUEUE_TIME : peer.download_queue_time,
            TORRENT.PEER.CONNECT : connected,
            TORRENT.PEER.PROGRESS : int(peer.progress * 100),
            TORRENT.PEER.IP : ip_joiner(peer.ip)
        }
        
        method = None

        if peer.source & peer.dht:
            method = TORRENT.TRACKER.STATS.DHT
        elif peer.source & peer.lsd:
            method = TORRENT.TRACKER.STATS.LSD
        elif peer.source & peer.pex:
            method = TORRENT.TRACKER.STATS.PEX

        temp[TORRENT.PEER.METHOD] = method

        is_seed = False

        if peer.flags & peer.seed:
            is_seed = True
        
        temp[TORRENT.PEER.SEED] = is_seed

        result[temp[TORRENT.PEER.IP]] = temp
    
    return result


# extract tracker data from list of trackers
def create_trackers_data(trackers):
    result = {}
    
    for tracker in trackers:

        temp = {
            TORRENT.TRACKER.VERIFIED : tracker[TORRENT.TRACKER.VERIFIED],
            TORRENT.TRACKER.TIER : tracker[TORRENT.TRACKER.TIER],
            TORRENT.TRACKER.SOURCE : tracker[TORRENT.TRACKER.SOURCE],
            TORRENT.TRACKER.STATE : TORRENT.TRACKER_STATE.NO_CONNECTION
        }

        result[tracker[TORRENT.TRACKER.URL]] = temp

    return result



def ip_joiner(info):
    return f"{info[0]}:{info[1]}"



