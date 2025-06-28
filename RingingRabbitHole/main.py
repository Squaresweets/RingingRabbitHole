from manim import *
from BellEnd.LineGenerator import *
from LineObject import *

class First_scene(Scene):
    def construct(self):
        # m = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        m = Method(8,"x38x14x1258x36x14x58x16x78,12",Calls("145","123",0,10,1),0,32)
        line = LineGenerator.generate_line([m], Composition(),1)

        lobject = LineObject(line)

        lobject.scale_to_fit_height(config.frame_height * 0.9)
        lobject.move_to(ORIGIN)

        lobject.set_line_visible(3, True)

        # self.add(lobject)
        self.play(lobject.reveal())
        self.play(lobject.animate_line_visible(5, True))
        self.play(lobject.table.animate(lag_ratio=0.01).shift(LEFT*2))
        self.play(lobject.animate_line_visible(3, False))
        # self.play(AnimationGroup(*[Flash(l) for l in lobject.get_bell_text_entries(2)], lag_ratio=0.1))
        self.play(lobject.unreveal())
        self.wait()


class Second_scene(Scene):
    def construct(self):
        t = Text("This is the second scene")
        self.play(Write(t))
        self.wait(2)
