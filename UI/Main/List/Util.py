
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from UI.Base.Items.Task.TaskItemControl import TaskItemControl


# General view item that is using in group/task list
class MItem(QtGui.QStandardItem):

    PRIVATE_ROLE = int(Qt.ItemDataRole.UserRole) + 1

    def __init__(self, info = None):
        super().__init__()

        if info:
            self.setData(info, self.PRIVATE_ROLE)


# Item delegate for task list
class ItemDel(QtWidgets.QStyledItemDelegate):

        def __init__(self, widget, x_m = 5, y_m = 3):
            super().__init__()

            self.WIDGET = widget
            self.border = 2
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

            state = bool(option.state & QtWidgets.QStyle.StateFlag.State_MouseOver)
            self.WIDGET.set_hover(state)

            state = bool(option.state & QtWidgets.QStyle.StateFlag.State_Selected)
            self.WIDGET.set_select(state)


            s = option.rect.size()
            p = option.rect.topLeft()


            p.setX(p.x() + self.x_m)
            p.setY(p.y() + self.y_m)

            s.setWidth(s.width() - 2 * (self.x_m))
            s.setHeight(s.height() - 2 * (self.y_m))

            self.WIDGET.resize(s)

            self.WIDGET.set_data(data)

            self.WIDGET.update()

            painter.save()

            painter.translate(p)

            self.WIDGET.render(painter)

            painter.restore()

