from .SaveUI import SaveUI


# Group dialog, Save section -- Control class
class SaveControl(SaveUI):

    def __init__(self):
        super().__init__()

        self.path_setting = None

        self.__connect_slots()


    def __connect_slots(self):
        self.optionBox.currentIndexChanged.connect(self.__change_stack)


    def set_setting(self, setting):
        self.path_setting = setting


    def set_size(self, size):
        self.pathBox.set_size(size)


    def __change_stack(self, index):
        self.stackLayout.setCurrentIndex(index)


    def get_path(self):
        index = self.stackLayout.currentIndex()
        path = None

        if index == self.CATEGORY_INDEX:
            cat = self.category.get_category()
            path = self.path_setting.get_path(cat)
        
        elif index == self.DIRECTORY_INDEX:
            path = self.pathBox.get_path()

        return path


