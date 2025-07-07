
from manim import *
from BellEnd.LineGenerator import *
from LineObject import *
from LineObjectGroup import *

class paragraph1(Scene):
    def construct(self):
        pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        plain = LineObject(LineGenerator.generate_line([pb])).set_line_visible(5, True)
        plain2 = LineObject(LineGenerator.generate_line([pb], initial_row=[1,2,4,3,5])).set_line_visible(5, True).next_to(plain)
        plain3 = LineObject(LineGenerator.generate_line([pb], initial_row=[1,3,2,5,4])).set_line_visible(5, True).next_to(plain2)
        self.add(plain, plain2, plain3)
        self.wait()