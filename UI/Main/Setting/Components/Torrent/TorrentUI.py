from PyQt5 import QtWidgets


# Setting Interface section -- UI class
class TorrentUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()


        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        
