
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QSize, Qt

from Utility.Gui import get_icon

# Label container for playing gif



class AnimLabel(QLabel):
    
    def __init__(self, file_path, width = 35, height = None, loading = False):
        super().__init__()

        self.loading = loading
        self.checkpoint_index = 0
        
        if not height:
            height = width

        self.__setup(file_path, width, height)
    


    def __setup(self, file_path, width, height):

        self.__movie = get_icon(file_path, gif = True)

        self.__movie.setBackgroundColor(Qt.GlobalColor.transparent)
        self.__movie.setPaused(True)
        self.__movie.setCacheMode(self.__movie.CacheMode.CacheNone)
        self.__movie.setScaledSize(QSize(width, height))
        self.__movie.jumpToNextFrame()

        self.setMovie(self.__movie)

        last = self.__movie.frameCount()
        self.checkpoints = [0, last // 2, last - 1]

        self.__movie.frameChanged.connect(self.__check_checkpoint)

    

    def __check_checkpoint(self, frame_number):
        if self.loading:
            return

        if frame_number == self.checkpoints[self.checkpoint_index]:
            self.stop()
            self.__increase_index()
    
    
    def __increase_index(self):
        if self.checkpoint_index < len(self.checkpoints) - 1:
            self.checkpoint_index += 1
        else:
            self.checkpoint_index = 0
            self.__movie.jumpToFrame(0)


    def start(self):
        self.__movie.setPaused(False)


    def stop(self):
        self.__movie.setPaused(True)



    def is_paused(self):
        return self.__movie.paused()




