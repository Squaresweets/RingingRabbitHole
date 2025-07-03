from manim import *
from BellEnd.LineGenerator import *
from LineObject import *
from LineObjectGroup import *

class paragraph1(Scene):
    def construct(self):
        pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        plain = LineObject(LineGenerator.generate_line([pb])).set_line_visible(3, True)

        pbText = Text("Plain Bob Doubles").scale(.9).next_to(plain, direction=UP)
        Group(pbText, plain).scale_to_fit_height(config.frame_height * 0.9).center()
        self.play(plain.reveal(), Write(pbText, run_time=1))
        self.play(Unwrite(pbText, run_time=0.4), plain.animate.center())

        arrow_1 = Arrow(start=.2*UP, end=.2*DOWN).next_to(plain.all_bell_texts[0], direction=UP, buff=0.1)
        self.play(FadeIn(arrow_1, run_time=0.2))
        self.play(arrow_1.animate.next_to(plain.all_bell_texts[4], direction=UP, buff=0.1))

        arrow_2 = Arrow(start=.2*LEFT, end=.2*RIGHT).next_to(plain.all_bell_texts[0], direction=LEFT, buff=0.1)
        self.play(FadeOut(arrow_1, run_time=0.2), FadeIn(arrow_2, run_time=0.2))
        self.play(arrow_2.animate.next_to(plain.all_bell_texts[200], direction=LEFT, buff=0.1))
        self.play(FadeOut(arrow_2, run_time=0.2))

        self.play(Indicate(plain.bell_lines[2]))

        first_row = VGroup(plain.all_bell_texts[i].primary_text.copy().set_opacity(1) for i in range(5))
        self.play(first_row.animate.next_to(plain, direction=RIGHT, buff=2).shift(UP*.5).scale(4))
        circle_1 = Circle(.3, color=HUNT_BELL_COLOR).move_to(first_row[0])
        circle_2 = Circle(.3, color=BELL_COLORS[1]).move_to(first_row[2])
        self.play(Create(circle_1))
        self.play(Create(circle_2))
        self.play(Uncreate(circle_1), Uncreate(circle_2))

        last_row = VGroup(plain.all_bell_texts[i+200].primary_text.copy().set_opacity(1) for i in range(5))
        self.play(last_row.animate.next_to(plain, direction=RIGHT, buff=2).shift(DOWN*.5).scale(4))
        self.play(plain.unreveal(), Unwrite(last_row), first_row.animate.center())

        dist = first_row[1].get_x() - first_row[0].get_x()
        extra_4 = first_row[3].copy()
        circles = [Circle(.1,fill_opacity=1, color=WHITE).move_to(first_row[i]).shift(DOWN*dist) for i in [0,1,3,4]]
        self.play(extra_4.animate.shift(DOWN*dist+LEFT*dist),
                  *[FadeIn(c) for c in circles])
        self.play(extra_4.animate.shift(2*RIGHT*dist),
                  circles[2].animate.shift(LEFT*dist),
                  circles[3].animate.shift(LEFT*dist))
        self.play(extra_4.animate.shift(LEFT*dist),
                  circles[3].animate.shift(RIGHT*dist))
        self.play(extra_4.animate.shift(2*LEFT*dist).set_color(RED),
                  circles[1].animate.shift(RIGHT*dist),
                  circles[2].animate.shift(RIGHT*dist))
        self.play(extra_4.animate.shift(RIGHT*dist).set_color(WHITE),
                  circles[1].animate.shift(LEFT*dist))
        extra_3 = first_row[2].copy().move_to(circles[2])
        self.play(Transform(circles[2], extra_3))
        self.play(Unwrite(first_row), Unwrite(extra_4), Unwrite(extra_3), *[FadeOut(c) for c in circles])

class paragraph2(Scene):
    def construct(self):
        m = Method(5,"5.1.5.1.5,125",Calls("1","123",0,10,1),0,10)
        leadEnds = [[1,2,3,4,5],[1,3,5,2,4],[1,5,4,3,2],[1,4,2,5,3]]
        lobjects = LineObjectGroup(*[LineObject(LineGenerator.generate_line([m], initial_row=le, lead_end_cap=1))
                    for le in leadEnds])

        lobjects.scale_to_fit_height(config.frame_height * 0.9).center()

        for l in lobjects:
            l.set_line_visible(3, True)

        self.play(lobjects.reveal())

        arrows = [Arrow(start=.2*LEFT, end=.2*RIGHT).next_to(lobjects[i].all_bell_texts[0], direction=LEFT, buff=0.1)
                  for i in range(4)]
        arrows.append(Arrow(start=.2*LEFT, end=.2*RIGHT).next_to(lobjects[3].all_bell_texts[50], direction=LEFT, buff=0.1))
        self.play(FadeIn(arrows[i]) for i in range(5))
        dist = lobjects[0].all_bell_texts[1].get_anchor_position()[0] - lobjects[0].all_bell_texts[0].get_anchor_position()[0]
        self.play(*[arrows[i].animate.shift(UP*dist) for i in range(5)], FadeOut(arrows[0]))
        self.play(*[arrows[i].animate.shift(DOWN*dist/2) for i in range(1,5)])
        self.play(FadeOut(arrows[i]) for i in range(1,5))

        self.play(lobjects.animate.arrange_horizontally().scale_to_fit_width(config.frame_width * 0.8))

        self.play(lobjects.animate_line_visible(2, True),
                  lobjects.animate_line_visible(4, True),
                  lobjects.animate_line_visible(5, True))

        center = lobjects.get_center()
        for l in lobjects[0].bell_lines:
            l.set_z_index(10)
        self.play(*[l.animate.move_to(center) for l in lobjects])

        grid_text = Text("Grid View", font_size=50).next_to(lobjects, direction=UP)
        self.play(Write(grid_text), *[FadeOut(lobjects[i], run_time=0.1) for i in range(1,4)])

        grid = lobjects[0]
        c = Composition(5, [CompositionPart('b')])
        new_line = LineGenerator.generate_line([m], c, 1)
        self.play(grid.animate_to_new_composition(new_line))

        last_row = VGroup(grid.all_bell_texts[i].primary_text.copy().set_opacity(1) for i in range(50,55))
        self.play(FadeIn(last_row, run_time=0.3))
        t = Text("Plain hunt lead head:", font_size=20).next_to(grid, direction=RIGHT, buff=2).shift(UP)
        self.play(last_row.animate.next_to(t, direction=DOWN), Write(t, run_time=.5))

        self.play(grid.animate_to_new_composition(LineGenerator.generate_line([m], lead_end_cap=1)))
        last_row2 = VGroup(grid.all_bell_texts[i].primary_text.copy().set_opacity(1) for i in range(50,55))
        self.play(FadeIn(last_row2, run_time=0.3))
        t2 = Text("Plain bob lead head:", font_size=20).next_to(grid, direction=RIGHT, buff=2).next_to(last_row, direction=DOWN*1.2)
        self.play(last_row2.animate.next_to(t2, direction=DOWN), Write(t2, run_time=.5))
        self.play(grid.unreveal(), Unwrite(grid_text), Unwrite(t, run_time=0.3), Unwrite(t2, run_time=0.3), Unwrite(last_row), Unwrite(last_row2))
