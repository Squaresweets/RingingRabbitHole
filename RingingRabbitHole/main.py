from manim import *
from BellEnd.LineGenerator import *
from LineObject import *

class First_scene(Scene):
    def construct(self):
        m = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        # m = Method(8,"x38x14x1258x36x14x58x16x78,12",Calls("145","123",0,10,1),0,32)
        line = LineGenerator.generate_line([m], Composition())

        lobject = LineObject(line)

        lobject.scale_to_fit_height(config.frame_height * 0.9)
        lobject.move_to(ORIGIN)

        lobject.set_line_visible(3, True)

        # self.add(lobject)
        self.play(lobject.reveal())
        # self.play(lobject.animate_line_visible(5, True))
        # self.play(lobject.leads[0].animate(lag_ratio=0.01).shift(LEFT*2),
        #           lobject.leads[1].animate(lag_ratio=0.01).shift(RIGHT*2))
        self.play(lobject.horizontal_leads())
        self.play(lobject.animate.scale_to_fit_width(config.frame_width * 0.8))
        # self.play(lobject.animate.scale(.7))
        # self.play(lobject.table.animate.scale(4))
        self.play(lobject.animate_line_visible(2, True),
                  lobject.animate_line_visible(4, True),
                  lobject.animate_line_visible(5, True),
                  lobject.animate_line_visible(3, False))
        # self.play(lobject.table.animate.arrange_in_grid(cols=line.stage, buff=0.15))
        center = lobject.get_center()
        self.play(*[l.animate.move_to(center) for l in lobject.leads])
        self.wait()
        self.play(lobject.unreveal())


class Second_scene(Scene):
    def construct(self):
        m = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        line = LineGenerator.generate_line([m], Composition())
        lobject = LineObject(line)
        lobject.scale_to_fit_height(config.frame_height * 0.9)
        lobject.move_to(ORIGIN)
        lobject.set_line_visible(3, True)
        self.play(lobject.reveal())

        m2 = Method(5,"3,1.5.1.5.1",Calls("145","123",0,10,1),0,10)
        line2 = LineGenerator.generate_line([m], Composition())
        lobject2 = LineObject(line2)
        lobject2.scale_to_fit_height(config.frame_height * 0.9)
        lobject2.move_to(ORIGIN)
        lobject2.set_line_visible(3, True)

        self.play(Transform(line, line2))

