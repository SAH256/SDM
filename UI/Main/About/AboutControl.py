import os, webbrowser as wb

from PyQt5 import QtWidgets, QtGui

from Utility.Core import SDM, ICONS
from Utility.Util import file_ops

from .AboutUI import AboutUI


# About Dialog Control
class About(AboutUI):

    def __init__(self, parent):
        super().__init__(parent)
        
        title = 'About SDM'
        self.setWindowTitle(title)

        self.__connect_slots()
        self.__setup()
    

    def __connect_slots(self):
        self.okBtn.clicked.connect(self.close)
        self.githubBtn.clicked.connect(self.__github_handler)

    def __setup(self):

        self.__setup_logo()
        self.__setup_info()
        self.__setup_attr()


    def __setup_logo(self):
        cache = QtGui.QPixmapCache()
        key = ICONS.LOGO
        pixmap = cache.find(key)
        
        if not pixmap:
            pixmap = QtGui.QPixmap(key)
            cache.insert(key, pixmap)
        
        self.logo_place.setPixmap(pixmap)


    
    def __setup_info(self):
        data = [
            ('Version', SDM.INFO.VERSION_STR),
            ('Python-Httpx', SDM.INFO.HTTPX_VERSION),
            ('PyQt5', SDM.INFO.PYQT_VERSION),
            ('Libtorrent', SDM.INFO.LIBTORRENT_VERSION),
            ('Openssl', SDM.INFO.OPENSSL_VERSION),
        ]

        text_name = 'info-text'
        data_name = 'info-data'

        for entry in data:
            text = QtWidgets.QLabel(entry[0] + ' : ')
            label = QtWidgets.QLabel(entry[1])
            
            text.setObjectName(text_name)
            label.setObjectName(data_name)

            self.infoLayout.addRow(text, label)

        self.update()

    def __setup_attr(self):
        file_name = 'attr.txt'
        file_path = os.path.join(SDM.PATHS.ICONS_PATH, file_name)
        text = file_ops(file_path, binary = False)
        
        self.attr_box.setText(text)
    

    def __github_handler(self):
        if SDM.INFO.PROJECT_LINK:
            wb.open(SDM.INFO.PROJECT_LINK)


