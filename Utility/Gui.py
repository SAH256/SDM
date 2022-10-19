from PyQt5.QtWidgets import QFileIconProvider
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon, QMovie

from .Core import SDM, CATEGORY, ICONS
from .Util import sizeChanger
from .Structure.Setting import Interface


# find icon based on file name or types
def iconFinder(file_name, is_magnet = False, is_folder = False):
    icon = None

    if is_magnet:
        icon = get_icon(ICONS.TASK.TORRENT)
    else:

        if file_name:
            provider = QFileIconProvider()

            if is_folder:
                icon = provider.icon(provider.IconType.Folder)
            else:
                info = QFileInfo(file_name)
                icon = provider.icon(info)
        else:
            icon = get_icon(ICONS.TASK.UNKNOWN)

    return icon


def get_icon(name, gif = False):
    name = SDM.PATHS.ICON_FOLDER + name
    
    if gif:
        return QMovie(name)

    return QIcon(name)


# find link in text and change text to html with <a> tags
def find_links(txt):
    pat = ' <br><br>'
    txt = txt.replace('\n', pat)
    words = txt.split(' ')

    result = []

    for word in words:
        if word.startswith('http') or word.startswith('ftp') or word.startswith('udp'):
            word = f'''<a href="{word}" style = "color : {Interface.COLORS.get('LINK')};font-weight : 600; font-style : italic;">here</a>'''

        result.append(word)
    
    return '<p>' + ' '.join(result) + '</p>'


# format transfer rate or limitation as infinite or arrow string
def get_transfer_str(down, up, speed = False, is_magnet = True):
    inf = '<span style="font-weight : 600;font-size : 18px;">∞</span>'

    _max = [-1, 2**20 * 10]

    if down in _max:
        down = inf
    else:
        down = sizeChanger(down)

    if up in _max:
        up = inf
    else:
        up = sizeChanger(up)

    text = f"{down}{'/s' if speed else ''}{' ↓   ' if is_magnet else ''}{up if is_magnet else ''}{'/s' if speed and is_magnet else ''}{' ↑' if is_magnet else ''}"
    
    return text



def findCategory(extension):
    extension = extension.lower()
    
    for row in SDM.EXTENSIONS:
        if extension in SDM.EXTENSIONS[row]:
            return row
    else:
        return CATEGORY.GENERAL






