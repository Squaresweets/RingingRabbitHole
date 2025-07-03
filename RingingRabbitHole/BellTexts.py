from manim import *
from BellEnd.Helper import *

FONT_SIZE = 12
class BellText(VMobject):
    def __init__(self, num, anchor):
        super().__init__()
        self.primary_text = Text(bell_value_to_string[num], font_size=FONT_SIZE)
        self.add(self.primary_text)

        self.num = num
        self.anchor = anchor

        self.add_updater(lambda m: m.shift(m.anchor.get_center() - m.primary_text.get_center()))
        self.update()
    
    def get_anchor_position(self):
        return self.anchor.get_center()
    
    def change_num(self, new_num, new_opacity):
        #Hacky way to work out how much we have been scaled
        scale = self.primary_text.width / Text(bell_value_to_string[self.num], font_size=FONT_SIZE).width
        self.primary_text.become(Text(bell_value_to_string[new_num], font_size=FONT_SIZE).scale(scale))
        self.primary_text.set_opacity(new_opacity)

        self.num = new_num
        return self
    
    def SWrite(self):
        # copy_to_animate = self.primary_text.copy()
        # self.primary_text.set_opacity(False)
        # return Succession(Write(copy_to_animate), UpdateFromFunc(None, lambda m: self.primary_text.set_opacity(True)))
        return Write(self.primary_text)

    def SUnwrite(self):
        copy_to_animate = self.primary_text.copy()
        self.primary_text.set_opacity(False)
        # return Succession(Unwrite(copy_to_animate), UpdateFromFunc(None, lambda m: self.primary_text.set_opacity(False)))
        return Unwrite(copy_to_animate)