
from manim import *
from BellEnd.LineGenerator import LineGenerator as lg
from LineObject import *
from LineObjectGroup import *

pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)

class paragraph1(Scene):
    def construct(self):
        plain_line = lg.generate_line([pb], lead_end_cap=2)
        bob_line = lg.generate_line([pb], Composition(5, [CompositionPart("b")]), 2)
        line_with = LineObject(plain_line).set_line_visible(5, True).scale_to_fit_height(config.frame_height * 0.9)
        self.play(line_with.reveal())

        b_text = Text("\"Bob!\"").shift(LEFT*4)
        s_text = Text("\"Single!\"").shift(RIGHT*4)
        self.play(Write(b_text))
        self.play(Write(s_text))
        self.play(Unwrite(s_text))

        self.play(line_with.animate_to_new_composition(bob_line))
        line_without = LineObject(plain_line).set_line_visible(5, True).shift(LEFT*1.5).scale_to_fit_height(config.frame_height * 0.9)

        without_a_call = Paragraph("Without a", "call", alignment="right").scale(0.8)
        without_a_call.shift(LEFT*3 - without_a_call.get_right()).to_edge(UP)
        with_a_call = Paragraph("With a", "call").scale(0.8)
        with_a_call.shift(RIGHT*3 - with_a_call.get_left()).to_edge(UP)
        self.play(Unwrite(b_text), Write(without_a_call), Write(with_a_call), line_without.reveal(), line_with.animate.shift(RIGHT*1.5))

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
                  FadeOut(without_a_call), FadeOut(with_a_call), FadeOut(with_descriptions), FadeOut(without_descriptions),
                  line_with.animate.to_edge(RIGHT).shift(LEFT*0.5),
                  line_without.animate.to_edge(RIGHT).shift(LEFT*3.5))

        self.play(*[line_with.animate_line_visible(i, True) for i in [2,3,5]],
                  *[line_without.animate_line_visible(i, True) for i in [2,3,5]])

        positions = [a.get_center() for a in anchors]
        self.play(Rotate(anchors[3], -PI/2, about_point=center),
                  anchors[2].animate.move_to(positions[3]))

        self.play(*[Unwrite(b.primary_text, run_time=0.1) for b in bell_texts], *[Unwrite(t, run_time=0.1) for t in texts], *[Uncreate(a, run_time=0.1) for a in arcs],
                  line_with.unreveal(), line_without.unreveal())

class paragraph2(Scene):
    def construct(self):
        c = Composition(5, [CompositionPart("p"), CompositionPart("p"), CompositionPart("b")])
        plain = LineObject(lg.generate_line([pb], c)).scale(2.5).set_all_lines_visible()
        leDist = plain.ruleoffs[0].get_y()-plain.ruleoffs[1].get_y()
        plain.shift(DOWN*3*leDist)
        self.play(plain.reveal())

        first = plain.get_row(0)
        second = plain.get_row(10)
        for i in range(5):
            first[i].set_color([HUNT_BELL_COLOR, BELL_COLORS[0], BELL_COLORS[1],BELL_COLORS[2],BELL_COLORS[3]][i])
            second[i].set_color([HUNT_BELL_COLOR, BELL_COLORS[1], BELL_COLORS[3],BELL_COLORS[0],BELL_COLORS[2]][i])
        self.play(FadeIn(first), FadeIn(second))
        self.play(first.animate.center().shift(LEFT*4+UP*1.5).scale(2), second.animate.center().shift(LEFT*4+DOWN*1.5).scale(2))

        whereEachGoes = [0,3,1,4,2]
        transitionLines = VGroup(*[Line(first[i].get_bottom(), second[whereEachGoes[i]].get_top(), buff=0.2).set_stroke(width=8) for i in range(5)])

        transitionLineCopies = VGroup()
        for i in range(5):
            c = plain.bell_lines[i].get_subcurve(0,1/7).clear_updaters()
            transitionLineCopies.add(c)
            transitionLines[i].set_color(c.get_color())
            self.play(c.animate.become(transitionLines[i]))

        self.play(plain.animate.shift(UP*leDist), FadeOut(first), FadeOut(second), transitionLines.animate.set_color(WHITE))

        first = plain.get_row(10)
        second = plain.get_row(20)
        for i in range(5):
            first[i].set_color([HUNT_BELL_COLOR, BELL_COLORS[1], BELL_COLORS[3],BELL_COLORS[0],BELL_COLORS[2]][i])
            second[i].set_color([HUNT_BELL_COLOR, BELL_COLORS[3], BELL_COLORS[2],BELL_COLORS[1],BELL_COLORS[0]][i])
        self.play(FadeIn(first), FadeIn(second))
        self.play(first.animate.center().shift(LEFT*4+UP*1.5).scale(2), second.animate.center().shift(LEFT*4+DOWN*1.5).scale(2))

        plain_text = Text("Plain:").move_to(transitionLines).to_edge(UP)
        bob_text = Text("Bob:").move_to([-plain_text.get_x(), plain_text.get_y(), 0])
        self.play(plain.animate.shift(UP*leDist), FadeOut(first), FadeOut(second), Write(plain_text), Write(bob_text))

        first = plain.get_row(20)
        second = plain.get_row(30)
        for i in range(5):
            first[i].set_color([HUNT_BELL_COLOR, BELL_COLORS[3], BELL_COLORS[2],BELL_COLORS[1],BELL_COLORS[0]][i])
            second[i].set_color([HUNT_BELL_COLOR, BELL_COLORS[3], BELL_COLORS[2],BELL_COLORS[0],BELL_COLORS[1]][i])
        self.play(FadeIn(first), FadeIn(second))
        self.play(first.animate.center().shift(RIGHT*4+UP*1.5).scale(2), second.animate.center().shift(RIGHT*4+DOWN*1.5).scale(2))

        whereEachGoes = [0,1,2,4,3]
        transitionLines = VGroup(*[Line(first[i].get_bottom(), second[whereEachGoes[i]].get_top(), buff=0.2).set_stroke(width=8) for i in range(5)])

        transitionLineCopies = VGroup()
        for i in range(5):
            c = plain.bell_lines[[0,4,3,2,1][i]].get_subcurve(2/7,3/7).clear_updaters()
            transitionLineCopies.add(c)
            transitionLines[i].set_color(c.get_color())
            self.play(c.animate.become(transitionLines[i]))

        self.play(FadeOut(first), FadeOut(second), transitionLines.animate.set_color(WHITE))

class paragraph3(Scene):
    def construct(self):
        def arrange_into_circle(m, center, radius, angle_offset=0):
            for i, item in enumerate(m.submobjects):
                angle = -2 * PI * i / len(m.submobjects) + PI/2 + angle_offset
                item.move_to(center + radius * np.array([np.cos(angle), np.sin(angle), 0]))
            return m
        
        lhs = VGroup([Text(t) for t in ["12345", "13524", "15432", "14253"]])
        arrange_into_circle(lhs, ORIGIN, 2)
        arrows = VGroup(Arrow(lhs[i].get_center(), lhs[(i+1)%4].get_center(), buff=0.7) for i in range(4))
        self.play(Write(lhs, run_time=2))
        self.play(*[Create(a) for a in arrows])
        
        shift_amount = 3.7
        self.play(lhs.animate.shift(LEFT*shift_amount), arrows.animate.shift(LEFT*shift_amount))

        blhs = VGroup([Text(t) for t in ["15423", "14352", "13245", "12534"]])
        arrange_into_circle(blhs, RIGHT*shift_amount, 2, PI/2)
        barrows = VGroup(Arrow(blhs[i].get_center(), blhs[(i+1)%4].get_center(), buff=0.7) for i in range(4))

        transition_arrow = Arrow(lhs[2].get_center(), blhs[0].get_center(), buff=1, color=BLUE)
        self.play(Create(transition_arrow))
        self.play(Write(blhs, run_time=2))
        self.play(*[Create(a) for a in barrows])

        plain_course = Text("Plain course:").next_to(lhs, direction=UP, buff=0.5)
        new_course = Text("New course:").next_to(blhs, direction=UP, buff=0.5)
        self.play(Write(plain_course), Write(new_course))

        self.play(lhs[0].animate.set_color(RED))
        self.play(blhs[2].animate.set_color(RED))
        self.play(Circumscribe(blhs[2][4]))

        self.play(Circumscribe(lhs[2][3])) #bell in 4ths place is uneffected
        self.play(Circumscribe(lhs[3]), Circumscribe(blhs[0])) #These two rows
        self.play(Circumscribe(lhs[3][4]), Circumscribe(blhs[0][4])) #Note that the bell which is in fourths place
        self.play(Circumscribe(lhs[0]), Circumscribe(blhs[1])) #Looking at the next lead
        for i in range(3):
            self.play(Circumscribe(blhs[1][[1,3,4][i]]))
            self.play(Circumscribe(lhs[0][[1,3,4][i]]))
        self.play(Circumscribe(lhs[0][2]), Circumscribe(blhs[1][2])) 
        self.play(Circumscribe(blhs[1])) 

        self.play(blhs[1].animate.become(Text("14235", color=RED).move_to(blhs[1])),
                  blhs[2].animate.become(Text("12543").move_to(blhs[2])),
                  blhs[3].animate.become(Text("15324").move_to(blhs[3])),
                  blhs[0].animate.become(Text("13452").move_to(blhs[0])),
                  transition_arrow.animate.become(Arrow(lhs[3].get_center(), blhs[1].get_center(), buff=1, color=BLUE)))
        
        self.play(Circumscribe(lhs[3][3]))

        disclaimer = Text("This is not how course heads work and is just to illustrate the point!").scale(0.5).to_edge(DOWN)
        self.play(blhs[1].animate.become(lhs[1]).set_color(RED).move_to(blhs[1]),
                  blhs[2].animate.become(lhs[2]).move_to(blhs[2]),
                  blhs[3].animate.become(lhs[3]).move_to(blhs[3]),
                  blhs[0].animate.become(lhs[0]).set_color(WHITE).move_to(blhs[0]),
                  FadeOut(transition_arrow), Write(disclaimer, run_time=1))
        
        self.play(*[Unwrite(a, run_time=1) for a in [lhs, blhs, plain_course, new_course, disclaimer]],
                  *[Uncreate(a, run_time=1) for a in [arrows, barrows]])

        

class paragraph4(Scene):
    def construct(self):
        plain_line = lg.generate_line([pb], lead_end_cap=2)
        line = LineObject(plain_line).set_line_visible(5, True).scale_to_fit_height(config.frame_height * 0.9)
        self.play(line.reveal())

        arrow = Arrow(start=.2*LEFT, end=.2*RIGHT).scale(2).next_to(line.all_bell_texts[95], direction=LEFT, buff=0.1)
        self.play(Create(arrow))

        first = line.get_row(0)
        second = line.get_row(19)
        self.play(FadeIn(first), FadeIn(second), FadeOut(arrow))
        self.play(first.animate.center().shift(RIGHT*4+UP*1.5).scale(2), second.animate.center().shift(RIGHT*4+DOWN*1.5).scale(2))

        whereEachGoes = [0,4,2,3,1]
        transitionLines = VGroup(*[Line(first[i].get_bottom(), second[whereEachGoes[i]].get_top(), buff=0.2).set_stroke(width=8) for i in range(5)])
        self.play(Create(transitionLines))

        positions = first.copy()
        self.play(first.animate.move_to(second), FadeOut(second))
        copies = VGroup(first[i].copy() for i in range(5))
        self.play(*[copies[i].animate.move_to(positions[whereEachGoes[i]]) for i in range(5)]) # can use where each line goes as it is its own inverse

        self.play(line.animate_to_new_composition(lg.generate_line([pb], lead_end_cap=2, initial_row=[1,5,3,4,2])))

        self.play(first.animate.move_to(line.get_row(19)).scale(.5), copies.animate.move_to(line.get_row(0)).scale(.5), FadeOut(transitionLines))
        self.play(FadeOut(first), FadeOut(copies))


        #Explanation:
        lines = [
            r"To explain this I first need to first define some notation:",
            r"A capital letter is a row. It can also be thought of as a permutation if you think of it as a permutation from rounds to that row. $XY$ is applying permutation $X$ to row $Y$. $I$ is rounds, also known as the identity row. Exponentiation means repeated application. $X^0=I$, $X^1=X$, $X^2=XX$, etc. $X^{-1}$ means the inverse permutation of X, such that $X^{-1}X=I$. $H$ is the first lead head of plain bob doubles. $A$ is the row we looked at in the previous section. Note that permutations do not commute (we cannot guarantee $XY=YX$).",
            r"So what we just visualised can be written as $H^xA^{-1}I$ where $H^x$ involves going forward $x$ leads until we get to the course head",
            r"The new row we are looking at is $B$, where $B=AH^n$ for some $n$.",
            r"Applying the same method as above:",
            r"$H^xB^{-1}I=H^x(AH^n)^{-1}I=H^xH^{-n}A^{-1}I=H^xA^{-1}I$ by absorbing $-n$ into the $x$ term.",
            r"And thus these two methods give the same solution as a course only has one course head. Don't worry if you don't get this now, I'll go into much more detail about this in the future"
        ]

        paragraph = VGroup(
            *[Tex(line, tex_environment="flushleft") for line in lines]
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.64).to_edge(LEFT)
        
        plain_line = lg.generate_line([pb])
        line = LineObject(plain_line).set_line_visible(5, True).scale_to_fit_height(config.frame_height * 0.9).to_edge(RIGHT)
        bits = VGroup()
        for i in range(3):
            bits.add(Text(["I","H","A"][i]).scale(0.4).next_to(line.all_bell_texts[[0,50,95][i]], direction=LEFT))
            

        self.play(Write(paragraph, run_time=1), line.reveal(), Write(bits, run_time=1))
        self.play(Unwrite(paragraph, run_time=1), line.unreveal(), Unwrite(bits, run_time=1))
        # self.add(paragraph, line, bits)