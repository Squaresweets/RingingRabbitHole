from manim import *
from BellEnd.Helper import *

class BellText(VMobject):
    def __init__(self, num, anchor):
        super().__init__()
        self.primary_text = Text(bell_value_to_string[num], font_size=10)
        self.add(self.primary_text)

        self.num = num
        self.anchor = anchor

        self.secondary_anchor = None
        self.secondary_text = None

        self.add_updater(lambda m: m.shift(m.anchor.get_center() - m.primary_text.get_center()))
        self.update()
    
    def add_secondary_bell(self, prev_pos):
        # self.secondary_anchor = VMobject().set_points_as_corners([ORIGIN]).move_to(prev_pos)
        self.secondary_anchor = Circle().scale(0.05).move_to(prev_pos)
        self.add(self.secondary_anchor)
    
    def show_extra_lead_head(self):
        if self.secondary_anchor == None:
            return

        self.secondary_text = BellText(self.num, self.secondary_anchor)
        self.secondary_text.primary_text.set_color(BLUE)
        self.secondary_text.set_opacity(self.get_stroke_opacity())
        self.add(self.secondary_text)
    
    def remove_extra_lead_head(self):
        if self.secondary_anchor == None:
            return
        
        self.remove(self.secondary_text)
        self.secondary_text = None
    
    def get_anchor_position(self):
        return self.anchor.get_center()
    
    def get_primary_and_secondary(self):
        return ([self.secondary_text] if self.secondary_text else []) + [self]