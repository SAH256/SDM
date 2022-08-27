from .ToolTab import ToolTab


class ToolControl(ToolTab):

    def add_item(self, item):
        if item:
            self.mainLayout.insertWidget(self.mainLayout.count() - 1, item)


    def add_space(self, d):
        self.mainLayout.addStretch(d)


    def set_spacing(self, s):
        self.mainLayout.setSpacing(s)

