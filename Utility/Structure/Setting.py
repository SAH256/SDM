import os

from PyQt5.QtCore import QDir
import libtorrent as lt

from Utility.Core import SDM, TORRENT, SETTING, CATEGORY, SECTIONS
from Utility.Structure.Task.Torrent import TorrentOptions
from Utility.Util import file_ops

# Setting is incomplete yet and does not used in Model completely
# in future updates maybe it will change...



class Network:
    
    def __init__(self):
        self.max_connection = 15
        self.default_part = 10
        self.timeout = 60


    def get_max_connection(self):
        return self.max_connection

    def get_default_part(self):
        return self.default_part
    
    def set_max_connection(self, value):
        if value > 0:
            self.max_connection = value
    

    def set_default_part(self, value):
        if value > 0:
            self.default_part = value



class Interface:
    CURRENT_PACKAGE = 'Default'
    CURRENT_THEME = 'Light'
    CURRENT_LANG = 'English'

    ICON_PACKAGES = ['Default']
    THEME_PACKAGES = ['Light']
    LANG_PACKAGES = ['English']


    def __init__(self):
        self.font = None
        self.base_font_size = 0
        self.primary_color = None
        self.secondary_color = None

    def change_icon_path(self):
        main_path = os.path.join(SDM.PATHS.ICONS_PATH, self.CURRENT_PACKAGE)
        paths = [main_path]

        for name in SECTIONS.NAMES:
            temp_path = os.path.join(main_path, name)
            paths.append(temp_path)
                
        QDir.setSearchPaths(SDM.PATHS.ICON_FOLDER, paths)


    def current_icon_pack(self):
        return self.CURRENT_PACKAGE
    
    def asset_pack_names(self):
        return self.ICON_PACKAGES
    
    def current_theme(self):
        return self.CURRENT_THEME
    
    def theme_names(self):
        return self.THEME_PACKAGES


    def current_lang(self):
        return self.CURRENT_LANG
    
    def lang_names(self):
        return self.LANG_PACKAGES
    
    def get_current_stylesheet(self):
        file_name = f'{self.current_theme()}.css'
        file_path = os.path.join(SDM.PATHS.ASSETS_FOLDER, SDM.PATHS.STYLES_FOLDER, file_name)
        
        return file_ops(file_path, binary = False)
        



class DirPath:

    DEFAULT_PATHS = {cat : os.path.join(SDM.PATHS.MAIN_PATH, cat) for cat in CATEGORY.CATEGORIES if cat}
    
    def __init__(self):
        self.user_paths = self.DEFAULT_PATHS.copy()


    def get_path(self, category):
        path = self.user_paths.get(category)

        if not path:
            path = self.DEFAULT_PATHS.get(category)


        if not path:
            path = self.DEFAULT_PATHS.get(CATEGORY.GENERAL)
        
        return path


    def set_path(self, cat, new_path):
        if cat in self.user_paths and os.path.exists(new_path):
            self.user_paths[cat] = new_path



class Torrent:

    def __init__(self):
        self.options = TorrentOptions()

        self.session_setting = {
            TORRENT.SETTING.USER_AGENT : f'python-client__{lt.__version__}',
            TORRENT.SETTING.LISTEN_INTERFACES : f"{self.options.listen_interface}:{self.options.port}",
            TORRENT.SETTING.DOWNLOAD_LIMIT : self.options.max_download_rate,
            TORRENT.SETTING.UPLOAD_LIMIT : self.options.max_upload_rate,
            TORRENT.SETTING.ALERT_MASK : lt.alert.category_t.all_categories,
            TORRENT.SETTING.OUTGOING_INTERFACES : self.options.outgoing_interface
        }


    def get_session_setting(self):
        return self.session_setting
    
    def get_option(self):
        return self.options


class Plugins:
    pass


class Setting:

    def __init__(self):
        self.network = Network()
        self.interface = Interface()
        self.dir_path = DirPath()
        self.torrent = Torrent()
        self.plugin = Plugins()

        self.__setup()



    def __setup(self):
        self.interface.change_icon_path()



    def get_client_setting(self):
        return {
            SETTING.NETWORK : self.network,
            SETTING.PATH : self.dir_path,
            SETTING.TORRENT : self.torrent
        }

    def get_view_setting(self):
        return {
            SETTING.INTERFACE : self.interface,
            # SETTING.PLUGINS : self.plugin
        }


    def get_network(self):
        return self.network

    def get_interface(self):
        return self.interface

    def get_path(self):
        return self.dir_path

    def get_torrent(self):
        return self.torrent

    def get_plugin(self):
        return self.plugin






