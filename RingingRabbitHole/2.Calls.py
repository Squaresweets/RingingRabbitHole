
from manim import *
from BellEnd.LineGenerator import LineGenerator as lg
from LineObject import *
from LineObjectGroup import *

pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
def arrange_into_circle(m, center, radius, angle_offset=0):
    for i, item in enumerate(m.submobjects):
        angle = -2 * PI * i / len(m.submobjects) + PI/2 + angle_offset
        item.move_to(center + radius * np.array([np.cos(angle), np.sin(angle), 0]))
    return m
def create_circle(text_arr, location, radius):
    lhs = VGroup([Text(t, color = RED if t[-1]=='5' else WHITE) for t in text_arr])
    arrange_into_circle(lhs, location, radius)
    arrows = [Arrow(lhs[i].get_center(), lhs[(i+1)%4].get_center(), buff=0.7) for i in range(4)]
    return VGroup(*lhs, *arrows)

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
        self.play(line.unreveal())


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
        self.wait()
        self.play(Unwrite(paragraph, run_time=1), line.unreveal(), Unwrite(bits, run_time=1))

class paragraph5(Scene):
    def construct(self):
        graph = VGroup()
        graph.add(create_circle(["12345", "13524", "15432", "14253"], RIGHT*3+UP*2, 2).scale(0.6))
        graph[0][6].set_opacity(0.3)
        graph.add(create_circle(["15423", "14352", "13245", "12534"], RIGHT*3+DOWN*2, 2).scale(0.6))
        graph[1][7].set_opacity(0.3)
        graph.add(create_circle(["14235", "12543", "15324", "13452"], LEFT*3+DOWN*2, 2).scale(0.6))
        graph[2][4].set_opacity(0.3)
        graph.insert(1, Arrow(graph[0][2].get_center(), graph[1][0].get_center(), buff=.25, color=BLUE))
        graph.insert(3, Arrow(graph[2][3].get_center(), graph[3][1].get_center(), buff=.75, color=BLUE))
        graph.insert(5, Arrow(graph[4][0].get_center(), graph[0][3].get_center(), buff=.5, color=BLUE))
        self.play(Write(graph))

        path = Polygon(graph[0][0].get_center(), graph[0][1].get_center(), graph[0][2].get_center(),
                       graph[2][0].get_center(), graph[2][1].get_center(), graph[2][2].get_center(), graph[2][3].get_center(),
                       graph[4][1].get_center(), graph[4][2].get_center(), graph[4][3].get_center(), graph[4][0].get_center(),
                       graph[0][3].get_center(), graph[0][0].get_center())
        d = Dot(graph[0][0].get_center())
        self.play(FadeIn(d))
        self.play(MoveAlongPath(d, path, run_time=3, rate_func=linear))
        self.play(FadeOut(d))
        self.play(Unwrite(graph))

class paragraph6(Scene):
    def construct(self):
        leadEnds = [[1,2,3,4,5],[1,3,5,2,4],[1,5,4,3,2],[1,4,2,5,3]]
        lobjects = LineObjectGroup(*[LineObject(LineGenerator.generate_line([pb], initial_row=le, lead_end_cap=1)) for le in leadEnds])
        for l in lobjects:
            l.set_line_visible(5, True)
        lobjects.arrange_horizontally().update(1)
        lobjects.scale_to_fit_width(config.frame_width * 0.8)

        texts = VGroup(Text(["Middle", "Out", "In", "Home"][i]).next_to(lobjects[i], direction=UP) for i in range(4))
        self.play(lobjects.reveal(), Write(texts, run_time=1))
        self.play(texts[1].animate.become(Text("Before").move_to(texts[1])))

        l = lobjects[3]
        t = texts[3]
        self.play(*[FadeOut(lobjects[i]) for i in range(3)], *[FadeOut(texts[i]) for i in range(3)], t.animate.set_x(0), l.animate.set_x(0))

        c = Composition(5, [CompositionPart("b")])
        self.play(l.animate_to_new_composition(LineGenerator.generate_line([pb], c, 1, leadEnds[3])))
        self.play(Circumscribe(l.get_bell_text_entry(5, 10)))
        self.play(Indicate(t))

        self.play(l.animate_to_new_composition(LineGenerator.generate_line([pb], c, 1, leadEnds[0])), t.animate.become(Text("Middle").move_to(t)))
        self.play(Circumscribe(l.get_bell_text_entry(5, 10)))

        pbm = Method(6,"x16x16x16,12",Calls("14","1234",0,12,1),0,12)
        minor = LineObject(LineGenerator.generate_line([pbm], c, 1)).scale_to_fit_height(l.height).next_to(l, buff=1).set_line_visible(6, True).set_line_visible(2, False).set_line_visible(3, False)
        minort = Text("Wrong").next_to(minor.bell_lines[5], direction=UP)
        self.play(minor.reveal(), Write(minort, run_time=1))

        self.play(l.animate_to_new_composition(LineGenerator.generate_line([pb], c, 1, leadEnds[1])),
                  minor.animate_to_new_composition(LineGenerator.generate_line([pbm], c, 1, [1,3,5,2,6,4])),
                  t.animate.match_x(minort), minort.animate.match_x(t))
        
        self.play(minort.animate.become(Text("Middle").move_to(minort)))
        note = Text("It is to ensure coursing order permutations are consistent across odd and even stages.").scale(0.5).to_corner(DL)
        self.play(Write(note, run_time=1))
        
        oldt = t.copy() #goofy
        t.become(minort)
        minort.become(oldt)
        self.play(Unwrite(minort, run_time=1), minor.unreveal(), Unwrite(note, run_time=1), t.animate.become(Text("Before").move_to(t)))

        cs = Composition(5, [CompositionPart("s")])
        self.play(l.animate_to_new_composition(LineGenerator.generate_line([pb], cs, 1, leadEnds[1])))
        self.play(Circumscribe(VGroup(l.get_bell_text_entry(5, 7), l.get_bell_text_entry(5, 8))))

        for i in range(5):
            self.play(l.animate_to_new_composition(LineGenerator.generate_line([pb], c, 1, leadEnds[[2, 1, 1, 0, 3][i]])), t.animate.become(Text(["In", "Out", "Thirds", "Fourths", "Fifths"][i]).move_to(t)))
        self.play(l.unreveal(), Unwrite(t))

class paragraph7(Scene):
    def construct(self):
        def create_comp(info):
            t = Table(info, include_outer_lines=True)
            t.remove(*t.get_vertical_lines())
            t.remove(t.horizontal_lines[0])
            t.remove(*[t.horizontal_lines[i] for i in range(3,len(info)+1)])
            return t
        t = create_comp([["2345","M","O","I"],
                        ["3245"," "," ","—"],
                        ["4235"," ","—"," "],
                        ["2345","—"," "," "]])
        self.play(Write(t))
        self.play(Circumscribe(VGroup(t.get_entries((1,i)) for i in [2,3,4])))

        note = Text("These are not true compositions!").scale(0.5).to_corner(DL)
        original = t.copy()
        self.play(t.animate.become(
            create_comp([["2345","M","O","I"],
                         ["3245"," "," ","s"],
                         ["3245"," ","—"," "],
                         ["(2435)","—"," "," "]])), FadeIn(note))
        self.play(t.animate.become(
            create_comp([["2345","M","O","I"],
                         ["2345"," "," ","2"],
                         ["4325"," ","—"," "],
                         ["3245","—"," "," "]])))
        self.play(t.animate.become(
            create_comp([["2345","M","O","I"],
                         ["2435"," "," ","-ss"],
                         ["3425"," ","—"," "],
                         ["4235","—"," "," "]])))
        self.play(t.animate.become(original), FadeOut(note))

        graph = VGroup()
        graph.add(create_circle(["12345", "13524", "15432", "14253"], RIGHT*3+UP*2, 2).scale(0.6))
        graph[0][6].set_opacity(0.3)
        graph.add(create_circle(["15423", "14352", "13245", "12534"], RIGHT*3+DOWN*2, 2).scale(0.6))
        graph[1][7].set_opacity(0.3)
        graph.add(create_circle(["14235", "12543", "15324", "13452"], LEFT*3+DOWN*2, 2).scale(0.6))
        graph[2][4].set_opacity(0.3)
        graph.insert(1, Arrow(graph[0][2].get_center(), graph[1][0].get_center(), buff=.25, color=BLUE))
        graph.insert(3, Arrow(graph[2][3].get_center(), graph[3][1].get_center(), buff=.75, color=BLUE))
        graph.insert(5, Arrow(graph[4][0].get_center(), graph[0][3].get_center(), buff=.5, color=BLUE))
        self.play(FadeIn(graph), t.animate.scale(0.6).to_corner(UL))
        self.play(*[t.get_entries((i,1)).animate.set_color(RED) for i in range(1,5)],
                  t.get_entries((2,4)).animate.set_color(BLUE),
                  t.get_entries((3,3)).animate.set_color(BLUE),
                  t.get_entries((4,2)).animate.set_color(BLUE))

        self.play(t.get_entries((1,1)).copy().animate(remover=True).move_to(graph[0][0][1:]))
        self.play(t.get_entries((2,1)).copy().animate(remover=True).move_to(graph[2][2][1:]))
        self.play(t.get_entries((3,1)).copy().animate(remover=True).move_to(graph[4][0][1:]))
        self.play(t.get_entries((4,1)).copy().animate(remover=True).move_to(graph[0][0][1:]))

        #iohh!