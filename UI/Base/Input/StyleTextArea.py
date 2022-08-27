
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

# Multi line text input style class



class TextArea(QtWidgets.QTextEdit):

    def __init__(self):
        super().__init__()

        self.setSizeAdjustPolicy(self.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.setAcceptRichText(False)
        

        self.padding = 5
        self.min_height = 30
        self.max_height = 75

        
        self.css_selector = 'css-class'

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


        self.textChanged.connect(self.__adjust_size)
        self.__adjust_size()

        self.__apply_style()


    def __adjust_size(self):

        height = 20
        size = self.document().size()

        if size.height():
            height = int(size.height())
        else:
            if self.text():
                height = 30
        

        height += 2 * self.padding

        if height > self.max_height:
            height = self.max_height

        elif height < self.min_height:
            height = self.min_height



        if height != self.height():
            self.setFixedHeight(height)



    def set_prop(self, prop):
        if prop:
            self.setProperty(self.css_selector, prop)
            self.__update()

    def __update(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
        
    
    def set_text(self, text):
        self.clear()
        self.insertPlainText(text)

        cursor = self.textCursor()
        cursor.setPosition(len(text))
        self.setTextCursor(cursor)


    def set_max_height(self, h):
        self.max_height = h
    
    def set_min_height(self, h):
        self.set_min_height = h


    def text(self):
        return self.toPlainText()


    def _reset(self):
        self.clear()

    def __apply_style(self):
        style = '''
        
        QTextEdit {
            border : none;
            padding : 5px;
            background-color : #eee;
        }

        QTextEdit:disabled {
            color : #333;
            background-color : #ccc;
        }

        QTextEdit:disabled[text=""] {
            border-bottom : 2px solid red;
        }

        QTextEdit:focus {
            background-color : #fff;
            border-bottom : 2px solid blue;
        }

        QTextEdit[css-class="error"] {
            border-bottom: 2px solid red;
        }

        QTextEdit[css-class="error"]:focus {
            border-bottom : 1px solid red;
        }

        
        '''

        self.setStyleSheet(style)
