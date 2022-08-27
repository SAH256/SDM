from PyQt5 import QtCore

from .AddMagnetUI import AddMagnetUI

from UI.Main.File.FileDialog import FileDialog

# Torrent / Magnet link add dialog -- Control class



class AddMagnetControl(AddMagnetUI):
    
    sendData = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)

        self.__connect_slots()


    def __connect_slots(self):
        self.linkBox.textChanged.connect(self.__state_handler)
        self.browseBtn.clicked.connect(self.__browse_handler)
        self.cancelBtn.clicked.connect(self.close)

        self.okBtn.clicked.connect(self.close)
        self.okBtn.clicked.connect(self.__link_handler)


    def __browse_handler(self):
            
        filters =  {
            'Torrent' : ['*torrent'],
        }

        d = FileDialog(self.windowTitle(), filters, False)

        result = d.exec()

        if result:
            data = d.selectedFiles()

            del d

            self.set_file_name(data[0])
            self.okBtn.setFocus()
        
    def set_file_name(self, file_name):
        self.linkBox.set_text(file_name)

    def reset(self):
        self.linkBox.clear()
    

    def __state_handler(self):
        text = self.linkBox.text()
        self.okBtn.setEnabled(bool(text))
            


    def __link_handler(self):
        link = self.linkBox.text()
        
        if link:
            self.sendData.emit(link)
            
    















