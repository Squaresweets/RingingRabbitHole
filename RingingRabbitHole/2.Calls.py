
from manim import *
from BellEnd.LineGenerator import LineGenerator as lg
from LineObject import *
from LineObjectGroup import *

class paragraph1(Scene):
    def construct(self):
        pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        plain_line = lg.generate_line([pb], lead_end_cap=2)
        bob_line = lg.generate_line([pb], Composition(5, [CompositionPart("b")]), 2)
        line_with = LineObject(plain_line).set_line_visible(5, True).scale_to_fit_height(config.frame_height * 0.9)
        self.play(line_with.reveal())

        b_text = Text("\"Bob!\"").shift(LEFT*4)
        s_text = Text("\"Single!\"").shift(RIGHT*4)
        self.play(Write(b_text))
        self.play(Write(s_text))

        self.play(line_with.animate_to_new_composition(bob_line))
        line_without = LineObject(plain_line).set_line_visible(5, True).shift(LEFT*1.5).scale_to_fit_height(config.frame_height * 0.9)

        without_a_call = Paragraph("Without a", "call", alignment="right").scale(0.8)
        without_a_call.shift(LEFT*3 - without_a_call.get_right()).to_edge(UP)
        with_a_call = Paragraph("With a", "call").scale(0.8)
        with_a_call.shift(RIGHT*3 - with_a_call.get_left()).to_edge(UP)
        self.play(Unwrite(b_text), Unwrite(s_text), Write(without_a_call), Write(with_a_call), line_without.reveal(), line_with.animate.shift(RIGHT*1.5))

        #Descriptions on the side
        without_descriptions = Paragraph("3/4 up", "Seconds", "3/4 down", "4 blows", alignment="right").scale(0.8)
        without_descriptions.shift(LEFT*3 - without_descriptions.get_right())

        with_descriptions = Paragraph("Make the bob", "Run out", "Run in", "4 blows").scale(0.8)
        with_descriptions.shift(RIGHT*3 - with_descriptions.get_left())
        for i,c in enumerate([BELL_COLORS[3], BELL_COLORS[1], BELL_COLORS[0], BELL_COLORS[2]]):
            without_descriptions[i].set_color(c)
            with_descriptions[i].set_color(c)
        self.play(Write(without_descriptions[0], run_time=1), Write(with_descriptions[0], run_time=1))

        self.play(line_without.animate_line_visible(2, True)) #Show the 2
        two_line = line_without.bell_lines[1].get_subcurve(0.5,1).clear_updaters()
        self.play(two_line.animate.shift(RIGHT*3).set_stroke(width=8)) #Move the fake line to the right
        self.play(FadeOut(two_line), line_without.animate_line_visible(2, False)) #Get rid of the 2

        for i in range(3):
            self.play(line_without.animate_line_visible([3,2,4][i], True),
                    line_without.animate_line_visible([5,3,2][i], False),
                    line_with.animate_line_visible([3,2,4][i], True),
                    line_with.animate_line_visible([5,3,2][i], False),
                    Write(without_descriptions[i+1], run_time=1),
                    Write(with_descriptions[i+1], run_time=1))

        radius = 2.5
        center = (-3,0,0)
        seconds = Paragraph("3nds", "place bell", alignment="center").move_to(center).shift(UP*radius).scale(0.8)
        down = Paragraph("2nds", "place bell", alignment="center").move_to(center).shift(RIGHT*radius).scale(0.8)
        fourths = Paragraph("4ths", "place bell", alignment="center").move_to(center).shift(DOWN*radius).scale(0.8)
        up = Paragraph("5ths", "place bell", alignment="center").move_to(center).shift(LEFT*radius).scale(0.8)
        texts = [seconds, down, fourths, up]

        arcs = VGroup()
        for i in range(4):
            arcs.add(Arc(angle=-PI/6, start_angle=-PI/6-i*PI/2, radius=radius*1).shift(center).add_tip())

        #Numbers
        layoutCircle = Circle(radius=radius*0.4).move_to(center)
        anchors = Group(*[Point().move_to(layoutCircle.point_from_proportion(0.25*i)).set_z_index(-1000) for i in range(4)])
        self.add(anchors)
        numbers = [2,3,5,4]
        bell_texts = VGroup(*[BellText(numbers[i], anchors[i]).scale(4).set_color(BELL_COLORS[numbers[i]-2]) for i in range(4)])
        self.add(bell_texts)

        self.play(*[Write(b.primary_text) for b in bell_texts],
                  *[Write(t) for t in texts],
                  *[Create(a) for a in arcs],
                  FadeOut(without_a_call), FadeOut(with_a_call), FadeOut(line_with), FadeOut(line_without),
                  without_descriptions.animate.next_to(with_descriptions, direction=LEFT).shift(RIGHT*0.5),
                  with_descriptions.animate.shift(RIGHT*0.5))
        plain_text = Text("Plain:").scale(0.8).next_to(without_descriptions[0], direction=UP)
        bob_text = Text("Bob:").scale(0.8).next_to(with_descriptions[0], direction=UP)
        self.play(Write(plain_text), Write(bob_text))


        positions = [a.get_center() for a in anchors]
        self.play(Rotate(anchors[3], -PI/2, about_point=center),
                  anchors[2].animate.move_to(positions[3]))

        self.play(*[Unwrite(b.primary_text, run_time=0.1) for b in bell_texts], *[Unwrite(t, run_time=0.1) for t in texts], *[Uncreate(a, run_time=0.1) for a in arcs], *[Unwrite(a, run_time=0.1) for a in [without_descriptions, with_descriptions, plain_text, bob_text]])