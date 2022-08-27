from PyQt5.QtWidgets import QFileDialog

from Utility.Core import CATEGORY, SDM

from .PathUI import PathUI


# Setting Path section -- Control class
class Path(PathUI):

    def __init__(self):
        super().__init__()

        self.path_data = None

        self.__connect_slots()
    

    def __connect_slots(self):
        self.categoryCombo.currentTextChanged.connect(self.__category_handler)
        self.browseBtn.clicked.connect(self.__browse_handler)
    

    def set_data(self, data):
        self.path_data = data
        self.__setup()
    

    def __setup(self):
        self.categoryCombo.addItems([x for x in CATEGORY.CATEGORIES if x])


    def __category_handler(self, cat):
        path = self.path_data.get_path(cat)
        self.pathInput.setText(path)

        self.__extension_handler(cat)
    

    def __extension_handler(self, cat):
        data = SDM.EXTENSIONS.get(cat)

        self.extension.clear()
        self.extension.setEnabled(bool(data))
        
        if data:
            self.extension.set_text(' '.join(data))


    def __browse_handler(self):
        path = QFileDialog.getExistingDirectory(self, caption = 'Select Save Path')

        self.__set_path(path)


    def __set_path(self, new_path):
        if new_path:
            self.pathInput.setText(new_path)


    def apply_changes(self):
        cat = self.categoryCombo.currentText()
        new_path = self.pathInput.text()
        extensions = self.extension.text().split(' ')

        self.path_data.set_path(cat, new_path)

        ext_packs = SDM.EXTENSIONS.get(cat)

        for ext in extensions:
            if ext and ext not in ext_packs:
                ext_packs.append(ext)


