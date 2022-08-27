import sys, os

import libtorrent as lt
from PyQt5 import Qt
import httpx as hx

from .Structure.Task.Base import TaskStatus


# THIS IS ALL CONST VARIABLES THAT MAY USED IN PROJECT
# ANY NEW CONST MAY BE ADDED HERE IF IT WILL USE IN MANY FILES




class DATA_UNIT:
    BYTE = 1
    KB = 2 ** 10
    MB = 2 ** 20
    GB = 2 ** 30
    TB = 2 ** 40
    
    UNITS = {
        BYTE : 'B',
        KB   : 'KB',
        MB   : 'MB',
        GB   : 'GB',
        TB   : 'TB',
    }




class PATTERNS:
    FILE_NAME_PATTERN = "[^/\\&\?]+\.\w{1,4}(?=([\?&].*$|$))"
    VALID_URL_PATTERN  = "(https?|ftps?)://([\w\d_\.]+)\.?:?([\d]+)?/?([\w\d?=\.\\//%_]+)?"
    DATE_PATTERN = '%a, %d %b %Y %H:%M:%S %Z'
    POSIX_PATTERN = '%A %d %b, %Y  %H:%M'


class LINK_TYPE :
    HTTP = 1
    MAGNET = 2

class STATES:
    PAUSED = 0
    RUNNING = 1
    COMPLETED = 2


class STATUS:

    PAUSED = TaskStatus('Paused')
    PENDING = TaskStatus('Pending...')
    COMPLETED = TaskStatus('Completed')


    CONNECTING = TaskStatus('Connecting', is_active = True)
    DOWNLOADING = TaskStatus('Downloading', is_active = True)
    WRITING = TaskStatus('Writing', is_active = True)
    BUILDING = TaskStatus('Building', is_active = True)

    QUEUED = TaskStatus('Queued', is_active = True)
    CHECKING = TaskStatus('Checking', is_active = True)
    METADATA = TaskStatus('Downloading Metadata', is_active = True)
    SEEDING = TaskStatus('Seeding', is_active = True)
    CHECKING_FR = TaskStatus('Checking Fastresume', is_active = True)

    CONNECT_ERROR = TaskStatus('Connection error', is_error = True)
    WEBPAGE_RECIEVED_ERROR = TaskStatus('Webpage Recieved', is_error = True)
    TIMEOUT_ERROR = TaskStatus('Timeout error', is_error = True)
    LINK_EXPIRED_ERROR = TaskStatus('Link expired', is_error = True)
    NOT_FOUND_ERROR = TaskStatus('File not found', is_error = True)
    SERVER_ERROR = TaskStatus('File not found', is_error = True)
    DUPLICATE_ERROR = TaskStatus('Duplicate Found', is_error = True)
    FILE_MISMATCH_ERROR = TaskStatus('File Mismatch', is_error = True)
    LOW_STORAGE_ERROR = TaskStatus('No disk space', is_error = True)
    
    ACTIVE = [CONNECTING, DOWNLOADING, CHECKING, METADATA, SEEDING, CHECKING_FR, QUEUED]
    ERROR = [CONNECT_ERROR, TIMEOUT_ERROR, LINK_EXPIRED_ERROR, LOW_STORAGE_ERROR]
    TORRENT_ORDER = [QUEUED, CHECKING, METADATA, DOWNLOADING, COMPLETED, SEEDING, '', CHECKING_FR]



class CATEGORY:
    ALL = None
    GENERAL = 'General'
    COMPRESSED = 'Compressed'
    DOCUMENT = 'Documents'
    PROGRAM = 'Programs'
    TORRENT = 'Torrent'
    IMAGE = 'Image'
    VIDEO = 'Video'
    AUDIO = 'Audio'

    CATEGORIES = [ALL, GENERAL, COMPRESSED, PROGRAM, AUDIO, IMAGE, VIDEO, DOCUMENT, TORRENT]


class FILTER:
    NAME = 0
    QUEUE = 1
    STATUS = 2
    CATEGORY = 3
    MIN_DATE = 4
    MAX_DATE = 5





class ACTIONS:
    REMOVE = 0
    PAUSE = 1
    RESUME = 2
    RENAME = 3
    FINISHED = 4
    PRIORITY = 5
    SETTING = 6
    SAVE_TORRENT = 7
    COPY_LINK = 8
    FORCE_REANNOUNCE = 9
    FORCE_RECHECK = 10
    OPEN = 11
    FOLDER = 12
    CHANGE_URL = 13
    SYSTEM = 14


class POPUP_TYPE:
    MESSAGE = 0
    DUPLICATE = 1
    DELETE = 2
    AUTH = 3
    CONFIRMATION = 4
    ADD = 6
    TORRENT_FILE = 7
    TEXTAREA = 8


class PRIORITY:
    LOW = 'Low'
    NORMAL = 'Normal'
    HIGH = 'High'

    PRIORITIES = {
        LOW : 2,
        NORMAL : 4,
        HIGH : 7
    }

    PRIORITIES_INDEX = dict([x[::-1] for x in PRIORITIES.items()])


class WEEK:
    SUNDAY = 'Sunday'
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'


    index_to_day = {
        '1' : MONDAY,
        '2' : TUESDAY,
        '3' : WEDNESDAY,
        '4' : THURSDAY,
        '5' : FRIDAY,
        '6' : SATURDAY,
        '7' : SUNDAY
    }


    day_to_index = dict([item[::-1] for item in index_to_day.items()])


class ERRORS:
    NO_LINK = 'No Link Provided...'
    DUPLICATE_TASK = 'Task with this data Exists..'
    METADATA_FAILED = 'Metadata Failed...'
    PARSE_FAILED = 'Parsing torrent file failed...'



class TASK_TYPE:
    FILE = 'File'
    TORRENT = 'Torrent'





class ADD_STATE:
    CONNECT = 'CONNECT'
    CONNECTING = 'CONNECTING'
    START = 'START'
    ADD = 'ADD'


class PLATFORMS:
    WINDOWS = 'win32'
    MAC = 'darwin'
    LINUX = 'linux2'


class DUPLICATE:
    NUMBER = 1
    OVERWRITE = 2
    OPEN_RESUME = 3
    MERGE_TRACKERS = 4


class SETTING:
    NETWORK = 0
    INTERFACE = 1
    PATH = 2
    LOCALIZATION = 3
    TORRENT = 4
    PLUGINS = 5


class QUEUE:

    class SETTING:
        ONE_TIME = 0
        PERIODIC = 1

        TIMER_TYPE = {
            ONE_TIME : 'One time download',
            PERIODIC : 'Periodic Synchronization',
        }

        SYSTEM_TYPE = 'System'
        USER_TYPE = 'User'



    class TIMER:
        DATE = 'Date'
        DAY = 'Day'
            
        TIMER_BASIS = [DATE, DAY]

        REPEAT = 'Repeat'


    class PROCESS:

        # SUB ACTIONS
        class SUB:
            MOVE_DIR = 'move_dir'
            BEEP = 'beep'
            MOVE_END = 'move_end'
            
        class POST:
            OPEN_FILE = 'open_file'
            EXIT_APP = 'exit_app'
            TURN_OFF = 'turn_off'
            FORCE_SHUT_DOWN = 'force_shut'

            SHUT_DOWN = 'Shutdown'
            HIBERNATE = 'Hibernate'
            SLEEP = 'Sleep'

            OPTIONS = [SHUT_DOWN, SLEEP, HIBERNATE]




# Base Const class
class SDM:

    class INFO:
        VERSION = (0, 0, 1)
        VERSION_STR = '.'.join([str(x) for x in VERSION])
        OPENSSL_VERSION = '3.0.0'
        PYQT_VERSION = Qt.PYQT_VERSION_STR
        LIBTORRENT_VERSION = lt.__version__
        HTTPX_VERSION = hx.__version__
        AUTHOR = 'SAH256'
        PROJECT_LINK = 'https://github.com/SAH256/SDM'

    class PATHS:
        APP_FOLDER = 'SDM'
        MAIN_FOLDER = 'Downloads'
        TEMP_FOLDER = 'Downloaded'
        STASH_FOLDER = 'Stash'
        SAVE_DATA_NAME = 'app_data.json'

        ASSETS_FOLDER = 'assets'
        ICON_FOLDER = 'Icons'
        DEPS_FOLDER = "Deps"
        PLUGINS_FOLDER = 'Plugins'

        MAIN_PATH = os.path.join(os.getenv('USERPROFILE'), MAIN_FOLDER)
        APP_PATH = os.path.join(os.getenv('APPDATA'), APP_FOLDER)

        TEMP_PATH = os.path.join(APP_PATH, TEMP_FOLDER)
        STASH_PATH = os.path.join(APP_PATH, STASH_FOLDER)
        PLUGINS_PATH = os.path.join(APP_PATH, PLUGINS_FOLDER)

        SAVE_DATA_PATH = os.path.join(APP_PATH, SAVE_DATA_NAME)

        ICONS_PATH = os.path.join(ASSETS_FOLDER, ICON_FOLDER)


    EXTENSIONS = {
        CATEGORY.COMPRESSED : ["zip", "rar", "7z", "iso", 'part'],
        CATEGORY.PROGRAM : ["exe", "dmg", "jar", "java", "py", "js"],
        CATEGORY.DOCUMENT : ["docx", "doc", "txt", "pptx", "xlsx", "pdf", "epub", 'psd', 'ai', 'srt'],
        CATEGORY.AUDIO : ["mp3", "m4a", "ogg", "wma"],
        CATEGORY.VIDEO : ["mp4", "mkv", "3gp", "wmv", 'avi'],
        CATEGORY.IMAGE : ['jpg', 'jpeg', 'tiff', 'svg', 'png', 'ico', 'heic'],
        CATEGORY.TORRENT : ['torrent']
    }


    COMMANDS = {

        QUEUE.PROCESS.POST.SHUT_DOWN : {
            PLATFORMS.WINDOWS : 'shutdown /s /t 015 ',
            PLATFORMS.MAC : '',
            PLATFORMS.LINUX : '',
        },

        QUEUE.PROCESS.POST.SLEEP : {
            PLATFORMS.WINDOWS : 'rundll32.exe powrprof.dll, SetSuspendState Sleep',
            PLATFORMS.MAC : '',
            PLATFORMS.LINUX : '',
        },

        QUEUE.PROCESS.POST.HIBERNATE : {
            PLATFORMS.WINDOWS : 'rundll32.exe powrprof.dll, SetSuspendState Hibernate',
            PLATFORMS.MAC : '',
            PLATFORMS.LINUX : '',
        }
    }




class ICONS:

    LOGO = SDM.PATHS.ICON_FOLDER + ':logo.png'

    class ACTION:
        ADD = ':add'
        MAGNET = ':magnet'
        RESUME = ':resume'
        PAUSE = ':pause'
        REMOVE = ':remove'
        SCHEDULER = ':scheduler'
        START = ':start'
        STOP = ':stop'
        TORRENT_SETTING = ':torrent_setting'

    class CATEGORY:
        ALL_DOWN = ':All_Download.png'
        COMPRESSED = ':Compressed.png'
        PROGRAM = ':Program.png'
        AUDIO = ':Audio.png'
        IMAGE = ':Image.png'
        VIDEO = ':Video.png'
        DOCUMENT = ':Document.png'
        TORRENT = ':Torrent.png'
        GENERAL = ':General.png'


    class HEADER:
        ALL = ':All.png'
        DOWNLOADING = ':Downloading.png'
        FINISHED = ':Finished.png'
        UNFINISHED = ':Unfinished.png'
        ERROR = ':Error.png'
        QUEUE = ':Queue.png'


    class SCHEDULER:
        TIMING = ':timing'
        FILE = ':queue_file'
        PROCESS = ':process'
        SETTING = ':setting'


    class TORRENT_SETTING:
        STATUS = ':status'
        DETAIL = ':detail'
        FILE = ':file'
        TRACKER = ':tracker'
        PEER = ':peer'
        SETTING = ':setting'
    

    class SETTING:
        NETWORK = ':network'
        INTERFACE = ':interface'
        PATH = ':path'
        TORRENT = ':torrent'
        PLUGIN = ':plugin'


    # if app use default icon for task
    class TASK:

        TORRENT = SDM.PATHS.ICON_FOLDER + ':Torrent_File.png'
        UNKNOWN = SDM.PATHS.ICON_FOLDER + ':Unknown_File.png'

    
    class ANIMATION:
        DOT_TABLE = SDM.PATHS.ICON_FOLDER + ':dot_table.gif'
        RHOMBUS = SDM.PATHS.ICON_FOLDER + ':rhombus.gif'
        SETTING = SDM.PATHS.ICON_FOLDER + ':setting.gif'


    class DIALOGS:
        ADD = SDM.PATHS.ICON_FOLDER + ':Add.png'
        BATCH = SDM.PATHS.ICON_FOLDER + ':Batch.png'
        GROUP = SDM.PATHS.ICON_FOLDER + ':Group.png'
        MAGNET = SDM.PATHS.ICON_FOLDER + ':Magnet.png'
        SETTINGS = SDM.PATHS.ICON_FOLDER + ':Settings.png'
        TIMER = SDM.PATHS.ICON_FOLDER + ':Timer.png'
        ABOUT = SDM.PATHS.ICON_FOLDER + ':About.png'
        
        



    class OTHER:
        ADD_1 = SDM.PATHS.ICON_FOLDER + ':add_1.png'
        ADD_2 = SDM.PATHS.ICON_FOLDER + ':add_2.svg'
        SUB = SDM.PATHS.ICON_FOLDER + ':Sub.svg'
        CALENDAR = SDM.PATHS.ICON_FOLDER + ':calendar.png'
        DOWN_ARROW = SDM.PATHS.ICON_FOLDER + ':Down-Arrow.svg'
        UP_ARROW = SDM.PATHS.ICON_FOLDER + ':Up-Arrow.svg'
        MOVE_DOWN = SDM.PATHS.ICON_FOLDER + ':move-down.png'
        MOVE_UP = SDM.PATHS.ICON_FOLDER + ':move-up.png'
        ONE_TIME = SDM.PATHS.ICON_FOLDER + ':one_time.png'
        PERIODIC = SDM.PATHS.ICON_FOLDER + ':periodic.png'
        TOTAL_DOWN = SDM.PATHS.ICON_FOLDER + ':t_down.svg'
        TOTAL_UP = SDM.PATHS.ICON_FOLDER + ':t_up.svg'
        TICK = SDM.PATHS.ICON_FOLDER + ':tick.svg'
        TRASH_1 = SDM.PATHS.ICON_FOLDER + ':trash_1.png'
        TRASH_2 = SDM.PATHS.ICON_FOLDER + ':trash_2.png'
        BROWSE_1 = SDM.PATHS.ICON_FOLDER + ':Browse_1.png'
        BROWSE_2 = SDM.PATHS.ICON_FOLDER + ':Browse_2.png'
        CATEGORY = SDM.PATHS.ICON_FOLDER + ':Category.png'
        FOLDER_1 = SDM.PATHS.ICON_FOLDER + ':Folder_1.png'
        INFO = SDM.PATHS.ICON_FOLDER + ':Info.png'
        CLOSE_WHITE = SDM.PATHS.ICON_FOLDER + ':close_white.png'
        GITHUB = SDM.PATHS.ICON_FOLDER + ':github.png'



# HTTP SECTION

class HTTP:

    class PROTOCOL:
        FTP = 'ftp'
        HTTP = 'http'


    class HEADER:
        SUPPORTED_RANGE = 'accept-ranges'
        CONTENT_LENGTH = 'content-length'
        DISPOSITION = 'content-disposition'
        FILE_NAME = 'filename'
        CONTENT_TYPE = 'content-type'
        LAST_MODIFIED = 'last-modified'
        ETAG = 'etag'
        RANGE = 'Range'
        IF_MATCH = 'If-Match'
        IF_UNMODIFIED = 'If-Unmodified-Since'
        NONE = 'none'

    class TYPE:
        HTML = 'text/html'
        

    class RESPONSE:

        OK = 200
        REDIRECT = 300

        CONNECT_ERROR = 0
        WEBPAGE_RECIEVED = 1
        DUPLICATE = 10
        UNAUTHORIZED = 401
        NOT_FOUND = 404
        EXPIRED = 410
        PRECONDITION = 412
        SERVER_ERROR = 500
        SERVER_UNAVAILABLE = 503

        ERROR_STATUS = {
            CONNECT_ERROR : STATUS.CONNECT_ERROR,
            WEBPAGE_RECIEVED : STATUS.WEBPAGE_RECIEVED_ERROR,
            DUPLICATE :     STATUS.DUPLICATE_ERROR,
            NOT_FOUND :     STATUS.NOT_FOUND_ERROR,
            EXPIRED :       STATUS.LINK_EXPIRED_ERROR,
            PRECONDITION :  STATUS.FILE_MISMATCH_ERROR,
            SERVER_ERROR :  STATUS.SERVER_ERROR,
            # SERVER_UNAVAILABLE : STATUS.
        }



# TORRENT SECTION

class TORRENT:
    FASTRESUME_EXT = '.fastresume'
    TORRENT_EXT = ".torrent"
    MAGNET_TAG = 'magnet:'

    SEEDER = 'Seeder'
    LEECHER = 'Leecher'

    REANNOUNCE = 'Reannounce'
    RECHECK = 'Recheck'

    PARSE_FAILED = 'Parsing torrent file failed...'

    class TYPE:
        TORRENT_FILE = 1
        MAGNET_LINK = 2

    class TRACKER:
        VERIFIED = 'verified'
        TIER = 'tier'
        SOURCE = 'source'
        STATE = 'state'
        URL = 'url'

        class STATS:
            DHT = 'dht'
            LSD = 'lsd'
            PEX = 'pex'

    class PEER:
        CLIENT = 'client'
        TOTAL_DOWN = 'total_down'
        TOTAL_UP = 'total_up'
        SPEED_UP = 'speed_up'
        SPEED_DOWN = 'speed_down'
        DOWN_QUEUE_TIME = 'down_queue_time'
        METHOD = 'method'
        SEED = 'seed'
        IP = 'ip'
        PROGRESS = 'progress'
        CONNECT = 'connect'
        
    class STATUS:
        STATUS = 'status'
        UPLOAD_SPEED = 'up_speed'
        DOWNLOAD_SPEED = 'down_speed'
        UPLOADED = 'uploaded'
        DOWNLOADED = 'downloaded'
        PROGRESS = 'progress'
        ETA = 'eta'
        SHARE_RATIO = 'share_ratio'
        TOTAL_PEERS = 'total_peers'
        TOTAL_SEEDS = 'total_seeds'
        SEEDERS = 'seeders'
        LEECHERS = 'leechers'
        SEEDING_TIME = 'seeding_time'
        ACTIVE_TIME = 'active_time'
        PIECES = 'pieces'
        AVAILABILITY = 'availability'
        
    class DETAIL:
        HASH = '_hash'
        NAME = 'name'
        SAVE_PATH = 'save_path'
        FILE_COUNT = 'file_count'
        FILE_SIZE = 'file_size'
        UPLOAD_LIMIT = 'up_limit'
        DOWN_LIMIT = 'down_limit'
        DATE_COMPLETED = 'date_completed'
        DATE_ADDED = 'date_added'
        TORRENT_DATE = 'torrent_date'
        LAST_SEEN = 'last_seen'
        COMMENT = 'comment'

    class TRACKER_STATE:
        DISABLED = 'Disabled'
        WORKING = 'Working'
        NOT_WORKING = 'Not Working'
        UPDATING = 'Updating'
        NO_CONNECTION = 'No Connection'

    class OPTIONS:
        SEQUENTIAL = lt.torrent_flags.sequential_download
        DISABLE_DHT = lt.torrent_flags.disable_dht
        DISABLE_LSD = lt.torrent_flags.disable_lsd
        DISABLE_PEX = lt.torrent_flags.disable_pex
        SEED_MODE = lt.torrent_flags.seed_mode
        SHARE_MODE = lt.torrent_flags.share_mode
        UPLOAD_MODE = lt.torrent_flags.upload_mode
        IP_FILTER = lt.torrent_flags.apply_ip_filter
        
        TEXTS = {
            SEQUENTIAL : 'Sequential Download',
            DISABLE_DHT : 'Disable DHT',
            DISABLE_LSD : 'Disable LSD',
            DISABLE_PEX : 'Disable PeX',
            SEED_MODE : 'Seed Mode',
            SHARE_MODE : 'Share Mode',
            UPLOAD_MODE : 'Upload Mode',
            IP_FILTER : 'IP Filter',
        }
        

    class SETTING:
        USER_AGENT = 'user_agent'
        LISTEN_INTERFACES = 'listen_interfaces'
        DOWNLOAD_LIMIT = 'download_rate_limit'
        UPLOAD_LIMIT = 'upload_rate_limit'
        ALERT_MASK = 'alert_mask'
        OUTGOING_INTERFACES = 'outgoing_interfaces'



class SECTIONS:
    ACTION = 'Actions'
    HEADER = 'Header'
    OPTION = 'Category'
    TASK = 'Files'
    SCHEDULER = 'Scheduler'
    TORRENT_SETTING = 'TorrentSetting'
    ANIMATION = 'Animation'
    DIALOGS = 'Dialogs'
    SETTING = 'Setting'
    OTHER = 'Other'

    NAMES = [ACTION, HEADER, OPTION, TASK, SCHEDULER, TORRENT_SETTING, ANIMATION, DIALOGS, SETTING, OTHER]


class SELECTORS:
    class STATES:
        CONFIRM = 'confirm'
        DANGER = 'danger'
        WARNING = 'warning'
        PLAIN = 'plain'


class SAVES:

    class TYPES:
        QUEUE = 'Queue'
        TASK = 'Task'
        SETTING = 'Setting'
    
    class SLOTS:
        ID = '_id'
        TYPE = '_type'
        URL = 'url'
        PART = 'part'
        RESUME = 'resume'
        ETAG = 'etag'
        NAME = 'name'
        QUEUE = 'queue'
        CATEGORY = 'category'
        PATH = 'path'
        DATE = 'date'
        METADATA = 'metadata'
        DOWNLOADED = 'downloaded'
        SIZE = 'size'
        STATE = 'state'
        DOWN_LIMIT = 'down_limit'
        UP_LIMIT = 'up_limit'
        SEQUENTIAL = 'sequential'
        PROGRESS = 'progress'
        PARAM = 'param'
        TIMER = 'timer'
        FILES = 'files'
        PROCESS = 'process'
        SETTING = 'setting'
        OPTIONS = 'options'



class TASK_OPTIONS:
    RETRY = 0
    PROXY = 1
    HIDDEN = 2

    TEXT = {
        RETRY   : 'Retry',
        PROXY   : 'Proxy',
        HIDDEN  : 'Hidden',
    }




