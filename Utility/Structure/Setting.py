import os, json, shutil as sh

from PyQt5.QtCore import QDir
from PyQt5.QtGui import QPixmapCache
from scss import Compiler
import libtorrent as lt

from Model.Saveable import Saveable


from Utility.Core import SDM, TORRENT, SETTING, CATEGORY, SECTIONS, SAVES
from Utility.Structure.Task.Torrent import TorrentOptions
from Utility.Engine.Graphic import apply_style
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
    THEME_PACKAGES = {}
    LANG_PACKAGES = ['English']
    
    COLORS = {}


    def __init__(self):
        self.font = None
        self.base_font_size = 0
        self.primary_color = None
        self.secondary_color = None

    
    def setup(self):
        self.__setup_theme()
        self.__setup_colors()
        self.__setup_icons()
        self.change_icon_path()
    

    def change_icon_path(self):
        main_path = os.path.join(SDM.PATHS.ICONS_PATH, self.CURRENT_PACKAGE)
        paths = [
            main_path,
            SDM.PATHS.CACHE_PATH,
            os.path.join(main_path, 'Const')
        ]
                
        QDir.setSearchPaths(SDM.PATHS.ICON_FOLDER, paths)


    def current_icon_pack(self):
        return self.CURRENT_PACKAGE
    
    def asset_pack_names(self):
        return self.ICON_PACKAGES
    
    def current_theme(self):
        return self.CURRENT_THEME
    
    def current_theme_path(self):
        return self.THEME_PACKAGES.get(self.CURRENT_THEME)
    
    def theme_names(self):
        names = list(self.THEME_PACKAGES.keys())
        names.sort(key = lambda x : x.count('Light'), reverse = True)
        
        return names


    def current_lang(self):
        return self.CURRENT_LANG
    
    def lang_names(self):
        return self.LANG_PACKAGES
    
    def set_theme(self, name):
        if name in self.THEME_PACKAGES:
            self.CURRENT_THEME = name

            QPixmapCache().clear()

            self.__setup_colors()
            self.__setup_icons()


    def get_current_stylesheet(self):
        file_name = 'Default.scss'
        file_path = os.path.join(self.current_theme_path(), file_name)

        return Compiler().compile(file_path)


    def __setup_theme(self):
        styles_folder = os.path.join(SDM.PATHS.ASSETS_FOLDER, SDM.PATHS.STYLES_FOLDER)
        sass_file = 'Default.scss'

        for entry in os.scandir(styles_folder):
            if entry.is_dir() and sass_file in os.listdir(entry.path):
                self.THEME_PACKAGES[entry.name] = entry.path
        

    def __setup_colors(self):
        file_name = 'metadata.json'
        file_path = os.path.join(self.current_theme_path(), file_name)
        
        data = {}
        
        with open(file_path) as file:
            data = json.load(file)
        
        Interface.COLORS.update(data)


    def __setup_icons(self):
        name = 'icon_data.json'
        style_name = 'icon_style.scss'

        data_path = os.path.join(self.current_theme_path(), name)
        style_path = os.path.join(self.current_theme_path(), style_name)

        if not os.path.exists(data_path):
            return

        style = Compiler().compile(style_path)

        out_path = SDM.PATHS.CACHE_PATH
        icon_data = None
        
        with open(data_path) as file:
            icon_data = json.load(file)


        for folder in icon_data:
            src_path = os.path.join(SDM.PATHS.ICONS_PATH, self.CURRENT_PACKAGE, folder)
            color_data = icon_data[folder]
            
            if color_data:
                apply_style(src_path, out_path, style, color_data)
            else:
                sh.copytree(src_path, out_path, dirs_exist_ok=True)


    def get_save_data(self):
        return {
            SAVES.SLOTS.LANG : self.CURRENT_LANG,
            SAVES.SLOTS.THEME : self.CURRENT_THEME,
            SAVES.SLOTS.ICON_PACK : self.CURRENT_PACKAGE,
        }
    
    def set_save_data(self, save_data):
        self.CURRENT_LANG = save_data.get(SAVES.SLOTS.LANG)
        self.CURRENT_THEME = save_data.get(SAVES.SLOTS.THEME)
        self.CURRENT_PACKAGE = save_data.get(SAVES.SLOTS.ICON_PACK)



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


class Setting(Saveable):

    def __init__(self):
        self.network = Network()
        self.interface = Interface()
        self.dir_path = DirPath()
        self.torrent = Torrent()
        self.plugin = Plugins()
        
        self.__setting_name = 'setting.json'

        self.__setup()



    def __setup(self):
        self.__restore_settings()

        self.interface.setup()



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


    def save_setting(self):
        setting_path = os.path.join(SDM.PATHS.APP_PATH, self.__setting_name)
        
        setting_data = {}
        
        for name, setting in {**self.get_client_setting(), **self.get_view_setting()}.items():
            if hasattr(setting, 'get_save_data'):
                setting_data[name] = setting.get_save_data()
        
        self._store_data(setting_path, setting_data)
        


    def __restore_settings(self):
        setting_path = os.path.join(SDM.PATHS.APP_PATH, self.__setting_name)

        save_data = self._retrieve_data(setting_path)
        
        for name, setting in {**self.get_client_setting(), **self.get_view_setting()}.items():
            setting_data = save_data.get(name)
            
            if setting_data:
                setting.set_save_data(setting_data)
            
        



