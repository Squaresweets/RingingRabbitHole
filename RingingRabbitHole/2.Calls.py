
from manim import *
from BellEnd.LineGenerator import LineGenerator as lg
from LineObject import *
from LineObjectGroup import *

class paragraph1(Scene):
    def construct(self):
        pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        plain = LineObject(lg.generate_line([pb], lead_end_cap=2)).set_line_visible(3, True)
        plain.scale_to_fit_height(config.frame_height * 0.9)
        self.add(plain)
        # self.play(plain.reveal())
        c = Composition(5, [CompositionPart("b")])
        # self.play(plain.animate_to_new_composition(lg.generate_line([pb], c, lead_end_cap=2)))
        c = Composition(5, [CompositionPart("s")])
        # self.play(plain.animate_to_new_composition(lg.generate_line([pb], c, lead_end_cap=2)))
        self.wait()