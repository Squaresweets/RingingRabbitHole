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

class CallText(VMobject):
    def __init__(self, text, far_text, second_farthest, opacity):
        super().__init__()
        self.text_object = Text("-" + text, font_size=FONT_SIZE)
        self.add(self.text_object)
        self.text = text

        def updater(m):
            new_pos = 2*far_text.get_anchor_position()-second_farthest.get_anchor_position()
            m.shift(new_pos - m.text_object.get_center())
        self.add_updater(updater)
        self.update()

        self.text_object.set_opacity(opacity)
    
    def change_text(self, new_text, new_opacity):
        #Hacky way to work out how much we have been scaled
        scale = self.text_object.width / Text(bell_value_to_string[self.num], font_size=FONT_SIZE).width
        self.text_object.become(Text(new_text, font_size=FONT_SIZE).scale(scale))
        self.text_object.set_opacity(new_opacity)

        self.text = new_text
        return self