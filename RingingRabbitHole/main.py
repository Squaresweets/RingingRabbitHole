from manim import *
from BellEnd.LineGenerator import *
from LineObject import *
from LineObjectGroup import *

class First_scene(Scene):
    def construct(self):
        m = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        leadEnds = [[1,2,3,4,5],[1,3,5,2,4],[1,5,4,3,2],[1,4,2,5,3]]
        lobjects = LineObjectGroup(*[LineObject(LineGenerator.generate_line([m], initial_row=le, lead_end_cap=1))
                    for le in leadEnds])

        lobjects.scale_to_fit_height(config.frame_height * 0.9)
        lobjects.move_to(ORIGIN)

        for l in lobjects:
            l.set_line_visible(3, True)

        self.play(lobjects.reveal())

        self.play(lobjects.animate.arrange_horizontally().scale_to_fit_width(config.frame_width * 0.8))

        self.play(lobjects.animate_line_visible(2, True),
                  lobjects.animate_line_visible(4, True),
                  lobjects.animate_line_visible(5, True))

        center = lobjects.get_center()
        self.play(*[l.animate.move_to(center) for l in lobjects])

        t = Text("Grid View", font_size=50).next_to(lobjects, direction=DOWN)
        self.play(Write(t))

        self.play(lobjects.unreveal(False), Unwrite(t))


class Second_scene(Scene):
    def construct(self):
        p = Method(5,"5.1.5.1.5,125",Calls("1","123",0,10,1),0,10)
        c = Composition(5, [CompositionPart('b')])
        plain = LineObject(LineGenerator.generate_line([p], lead_end_cap=1))
        plain.scale_to_fit_height(config.frame_height * 0.9)
        # plain.set_line_visible(3, True)
        # plain.set_line_visible(2, True)
        # plain.set_line_visible(4, True)
        plain.set_line_visible(5, True)
        self.play(plain.reveal())

        self.play(plain.animate_to_new_composition(LineGenerator.generate_line([p], c, 1)), run_time=0.3)
        self.wait()