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
        self.play(first_row.animate.next_to(plain, direction=RIGHT, buff=2).scale(4))
        circle_1 = Circle(.3, color=HUNT_BELL_COLOR).move_to(first_row[0])
        circle_2 = Circle(.3, color=BELL_COLORS[1]).move_to(first_row[2])
        self.play(Create(circle_1),  Create(circle_2))
        self.play(Uncreate(circle_1), Uncreate(circle_2))

        last_row = VGroup(plain.all_bell_texts[i+200].primary_text.copy().set_opacity(1) for i in range(5))
        self.play(last_row.animate.next_to(first_row, direction=DOWN).scale(4), first_row.animate.shift(UP))