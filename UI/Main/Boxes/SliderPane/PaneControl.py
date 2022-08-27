
from .PaneUI import PaneUI


# Panel for handling sliders -- Control class
class PaneControl(PaneUI):

    def __init__(self):
        super().__init__()

        self.downSlider.set_value(2**20 * 10)
        self.set_visible()


    def set_visible(self, part = True, down = True, up = False):
        self.partSlider.setVisible(part)
        self.downSlider.setVisible(down)
        self.upSlider.setVisible(up)
    
    def set_part(self, value):
        self.partSlider.set_value(value)

    def get_part(self):
        return self.partSlider.get_value()

    def get_down_limit(self):
        return self.downSlider.get_value()

    def get_up_limit(self):
        return self.upSlider.get_value()
    
    def set_up_limit(self, value):
        self.upSlider.set_value(value)
    
    def set_down_limit(self, value):
        self.downSlider.set_value(value)

    def _reset(self):
        self.partSlider._reset()
        self.downSlider._reset()
        self.upSlider._reset()






