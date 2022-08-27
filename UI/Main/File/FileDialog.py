
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


# File select dialog
class FileDialog(QtWidgets.QFileDialog):

    def __init__(self, title, filters = {}, multi_file = False):
        super().__init__(None, title)

        mode = self.FileMode.ExistingFile

        if multi_file:
            mode = self.FileMode.ExistingFiles

        self.setFileMode(mode)

        filters['All Files'] = ['*']

        self.set_filters(filters)
    
    def set_filters(self, filters):
        result = []

        if isinstance(filters, dict):
            
            for name, data in filters.items():
                temp = '('

                for ext in data:
                    temp += ext
                
                temp = name + ' ' + temp + ')'

                result.append(temp)
            
            self.setNameFilters(result)

