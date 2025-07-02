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
        self.remove(self.primary_text)

        self.primary_text = Text(bell_value_to_string[new_num], font_size=FONT_SIZE)
        self.primary_text.set_opacity(new_opacity)
        self.add(self.primary_text)

        self.num = new_num
        return self