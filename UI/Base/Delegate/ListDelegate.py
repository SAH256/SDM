from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from .Items import MItem


# Item delegate for task list
class ListItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, widget, x_m = 5, y_m = 3):
        super().__init__()

        self.WIDGET = widget
        self.border = 1
        self.x_m = x_m
        self.y_m = y_m


    def paint(self, painter, option, index):
        painter.setRenderHint(QtGui.QPainter.RenderHint.HighQualityAntialiasing)

        option.showDecorationSelected = False

        data = index.data(MItem.PRIVATE_ROLE)

        if not data:
            return

        if not index.isValid():
            return super().paint(painter, option, index)

        style = option.widget.style() if option.widget else QtWidgets.QApplication.style()

        style.drawControl(QtWidgets.QStyle.ControlElement.CE_ItemViewItem, option, painter, option.widget)

        if hasattr(self.WIDGET, 'set_hover'):
            state = bool(option.state & QtWidgets.QStyle.StateFlag.State_MouseOver)
            self.WIDGET.set_hover(state)

        if hasattr(self.WIDGET, 'set_selected'):
            state = bool(option.state & QtWidgets.QStyle.StateFlag.State_Selected)
            self.WIDGET.set_selected(state)


        s = option.rect.size()
        p = option.rect.topLeft()


        p.setX(p.x() + self.x_m)
        p.setY(p.y() + self.y_m)

        s.setWidth(s.width() - 2 * self.x_m)
        s.setHeight(s.height() - 2 * self.y_m)

        self.WIDGET.resize(s)

        self.WIDGET.set_data(data)

        self.WIDGET.update()

        painter.save()

        painter.translate(p)

        self.WIDGET.render(painter)

        painter.restore()










