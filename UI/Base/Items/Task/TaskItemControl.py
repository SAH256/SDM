from PyQt5 import QtGui, QtCore

from Utility.Gui import iconFinder, get_transfer_str
from Utility.Util import sizeChanger
from Utility.Calcs import format_remain_time
from Utility.Core import LINK_TYPE, STATUS, STATES

from .TaskItem import TaskItem

# Task Item Control class


class TaskItemControl(TaskItem):

    def __init__(self, parent):
        super().__init__(parent)

        self.info = None

        self.resume_prop = 'resume'
        self._expand()


    def __setup(self):
        is_magnet = self.info._type == LINK_TYPE.MAGNET
        name = ''

        if self.info.name:
            name = self.info.name

        if (self.info.metadata and self.info.resume) or is_magnet:
            self.nameLabel.setProperty(self.css_prop, self.resume_prop)
            self.update()

        self.nameLabel.setText(name)

        pixmap = self.get_pixmap(name, is_magnet)
        self.set_icon(pixmap)

        status = ''
        remaining = ''

        if  (self.info.state == STATES.RUNNING)      and \
            (self.info.status == STATUS.DOWNLOADING) and \
            (self.info.status != STATUS.BUILDING):
            
            status = get_transfer_str(self.info.download_speed, self.info.upload_speed, True, is_magnet)

            remaining = 'N/A'

            if self.info.eta > -1:
                remaining = format_remain_time(self.info.eta)
            
        else:
            status = str(self.info.status)

        self.status.setText(status)
        self.remained_time.setText(remaining)

        na = 'N/A'

        total_size = na
        downloaded = sizeChanger(self.info.downloaded)

        if self.info.total_size:
            total_size = sizeChanger(self.info.total_size)

        progress = f'{downloaded} / {total_size}'
        self.progress.setText(progress)

        percent = f'({round(self.info.progress * 100, 2):.2f} %)'
        self.percentage.setText(percent)


    def get_pixmap(self, name, is_magnet):
        super().get_pixmap()
        
        key = 'magnet'

        if not is_magnet:
            key = name.split('.')[-1]

        pixmap = self.cache.find(key)

        if not pixmap:
            icon = iconFinder(name, is_magnet)
            pixmap = icon.pixmap(self.big_size, self.big_size)
            self.cache.insert(key, pixmap)

        return pixmap


    def update(self):
        self.style().unpolish(self.nameLabel)
        self.style().polish(self.nameLabel)
        super().update()


    def paintEvent(self, event):
        super().paintEvent(event)
        
        if self.info and not self.selected and not self.hover:

            # rgb(165 222 255)
            # rgb(139 212 239)
            # rgb(161 230 255)
            # rgb(200 255 210)
            # rgb(255 190 190)

            error_color = QtGui.QColor(255, 190, 190)
            select_color = QtGui.QColor(165, 222, 225)
            build_color = QtGui.QColor(200, 255, 210)
            down_color = QtGui.QColor(139, 212, 239, 125)

            p = QtGui.QPainter(self)

            color = down_color

            rect = self.rect()
            rect = QtCore.QRectF(rect)

            status = self.info.status

            if status and status.is_error():
                color = error_color
            else:
                s = round(rect.width() * self.info.progress)
                rect.setWidth(s)

            if status == STATUS.BUILDING or self.info.state == STATES.COMPLETED:
                color = build_color


            r = QtGui.QPainterPath()
            r.addRoundedRect(rect, 3, 3)
            p.fillPath(r, color)


    def set_data(self, data):
        self.info = data
        self.__setup()
            
