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

class paragraph3(Scene):
    def construct(self):
        texts = VGroup(Text("Making seconds:"), Text("Dodging:"), Text("Four blows behind:")).center().scale(0.7).shift(UP*3)
        texts[0].shift(LEFT*4.5)
        texts[2].shift(RIGHT*4.5)
        self.play(Write(t, run_time=1) for t in texts)

        seconds_line = VMobject(stroke_width=10).set_points_as_corners([(0,0,0), (1,-1,0), (1,-2,0), (1,-2,0)]).center().match_x(texts[0])
        self.play(Create(seconds_line))
        self.play(seconds_line.animate.set_points_as_corners([(0,0,0), (1,-1,0), (1,-2,0), (0,-3,0)]).center().match_x(texts[0]))
        self.play(seconds_line.animate.set_points_as_corners([(0,0,0), (1,-1,0), (1,-2,0), (2,-3,0)]).center().match_x(texts[0]))

        pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        plain = LineObject(LineGenerator.generate_line([pb], lead_end_cap=2)).match_x(texts[0]).scale(1.5)
        plain.set_line_visible(3, True)
        self.play(plain.reveal(),
                  seconds_line.animate.set_points_as_corners([plain.get_bell_text_entry(3,i).get_anchor_position() for i in range(8,12)]))
        self.play(FadeOut(seconds_line))

        up_dodge_line = VMobject(stroke_width=10).set_points_as_corners([(0,0,0),(0,0,0), (1,-1,0), (0,-2,0), (1,-3,0), (1,-3,0)]).scale(0.6).center()
        down_dodge_line = up_dodge_line.copy().flip()
        up_dodge_line.shift(LEFT*0.6)
        down_dodge_line.shift(RIGHT*0.6)
        up_text = Text("Up:").scale(0.5).next_to(up_dodge_line, direction=UP)
        down_text = Text("Down:").scale(0.5).match_x(down_dodge_line).match_y(up_text)
        self.play(Create(up_dodge_line), Create(down_dodge_line), Write(up_text, run_time=0.5), Write(down_text, run_time=0.5))

        up_example = LineObject(LineGenerator.generate_line([pb], lead_end_cap=2)).scale(1.5)
        up_example.set_line_visible(5, True)
        self.play(up_example.reveal(),
                  up_dodge_line.animate.set_points_as_corners([up_example.get_bell_text_entry(5,i).get_anchor_position() for i in range(7,13)]),
                  Unwrite(down_text), Uncreate(down_dodge_line), Unwrite(up_text))
        arrow = Arrow(start=.2*LEFT, end=.2*RIGHT).next_to(up_example.all_bell_texts[35], direction=LEFT, buff=0.1)
        self.play(FadeIn(arrow, run_time=0.2))
        for i in range(40, 61, 5):
            self.play(arrow.animate(run_time=0.3).next_to(up_example.all_bell_texts[i], direction=LEFT, buff=0.1))
        self.play(FadeOut(arrow, run_time=0.2), FadeOut(up_dodge_line))

        right = Arrow(start=.2*LEFT, end=.2*RIGHT).scale(2).next_to(up_example, direction=DOWN)
        up_text = Text("Up/Out").scale(0.6).next_to(right, direction=RIGHT)

        left = right.copy().flip().next_to(right, direction=DOWN)
        down_text = Text("Down/In").scale(0.6).next_to(left, direction=LEFT)
        self.play(Create(left), Write(down_text), Create(right), Write(up_text))

        self.play(Uncreate(left), Unwrite(down_text), Uncreate(right), Unwrite(up_text))
        self.play(up_example.animate_line_visible(2, True))

        fourths_line = VMobject(stroke_width=10).set_points_as_corners([(0,0,0), (1,-1,0), (1,-2,0), (1,-2,0), (1,-2,0), (0,-3,0)]).center().match_x(texts[2])
        self.play(Create(fourths_line))

        t = Text("Place").scale(0.7)
        t.add_updater(lambda m: m.next_to(fourths_line, direction=DOWN))

        self.play(Write(t, run_time=0.3))
        self.play(fourths_line.animate.set_points_as_corners([(0,0,0), (1,-1,0), (1,-2,0), (1,-3,0), (1,-4,0), (0,-5,0)]).center().match_x(texts[2]),
                  t.animate.become(Paragraph("Long place", "(4 blows)", alignment="center").scale(0.6)))

        fourths_example = LineObject(LineGenerator.generate_line([pb], lead_end_cap=2)).scale(1.5).match_x(texts[2])
        fourths_example.set_line_visible(4, True)
        self.play(fourths_example.reveal(),
                  fourths_line.animate.set_points_as_corners([fourths_example.get_bell_text_entry(4,i).get_anchor_position() for i in range(7,13)]),
                  FadeOut(t))
        self.play(FadeOut(fourths_line))

        self.play(plain.unreveal(), up_example.unreveal(), fourths_example.unreveal(),
                  *[Unwrite(t, run_time=1) for t in texts])

class paragraph4(Scene):
    def construct(self):
        pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        plain = LineObject(LineGenerator.generate_line([pb], lead_end_cap=1)).center().scale_to_fit_height(config.frame_height * 0.9)
        plain.set_line_visible(5, True)
        self.play(plain.reveal())
        last_row = plain.get_row(10)
        self.play(last_row.animate.center().scale(1.25), plain.unreveal())

        m = Method(5,"5.1.5.1.5,125",Calls("1","123",0,10,1),0,10)
        leadEnds = [[1,2,3,4,5],[1,3,5,2,4],[1,5,4,3,2],[1,4,2,5,3]]
        lobjects = LineObjectGroup(*[LineObject(LineGenerator.generate_line([m], initial_row=le, lead_end_cap=1)) for le in leadEnds])
        for right_of_rounds in lobjects:
            right_of_rounds.set_line_visible(5, True)
        lobjects.arrange_horizontally().update(1)
        lobjects.scale_to_fit_width(config.frame_width * 0.8)

        self.play(lobjects.reveal(), last_row.animate.become(lobjects[1].get_row(0)))
        self.play(FadeOut(last_row))

        rounds_text = lobjects[0].get_row(0)
        self.play(rounds_text.animate.center().to_edge(UP, buff=0.8).shift(LEFT*2).scale(1.2))
        pblead_text = lobjects[1].get_row(0)
        self.play(pblead_text.animate.center().to_edge(UP, buff=0.8).shift(RIGHT*2).scale(1.2))
        # We need to align it vertically
        right_of_rounds = rounds_text.get_right()
        a = Arrow(right_of_rounds, [pblead_text.get_left()[0], right_of_rounds[1], 0])
        self.play(Create(a))

        fancyLines = VGroup()
        for i in range(3):
            p1b = lobjects[i].all_bell_texts[54].get_anchor_position() + RIGHT*0.4
            p2b = lobjects[i+1].all_bell_texts[0].get_anchor_position() + LEFT*0.4
            bezier = CubicBezier(p1b, p1b + .8 * RIGHT, p2b - .8 * RIGHT, p2b)
            t1 = Triangle(color=WHITE, fill_opacity=1).scale(0.1).rotate(-PI/2).move_to(bezier.get_end())
            t2 = Triangle(color=WHITE, fill_opacity=1).scale(0.1).rotate(PI/2).move_to(bezier.get_start())
            fancyLines.add(bezier, t2, t1)
        self.play(FadeIn(fancyLines))
        self.play(FadeOut(fancyLines))

        self.play(Indicate(lobjects[0].bell_lines[4], color=RED), Indicate(rounds_text[4], color=RED))
        self.play(Indicate(lobjects[1].bell_lines[4], color=RED), Indicate(pblead_text[2], color=RED))

        lead_head_positions = [5,3,2,4]
        for i in range(1,4):
            n = lead_head_positions[i]
            pn = lead_head_positions[i-1]
            self.play(lobjects[0].animate_line_visible(n, True), lobjects[0].animate_line_visible(pn, False))
            fl = lobjects[0].bell_lines[n-1].copy().clear_updaters()
            self.play(fl.animate.move_to(lobjects[i].bell_lines[n-1]))
            self.play(FadeOut(fl))
            if i == 1:
                self.play(Unwrite(rounds_text), Unwrite(pblead_text), Uncreate(a))
        self.play(lobjects[0].animate_line_visible(5, True), lobjects[0].animate_line_visible(4, False))

        # last_rounds = lobjects[3].get_row(10)
        # self.play(FadeIn(last_rounds))
        # self.play(Indicate(last_rounds))
        # self.play(FadeOut(last_rounds))
        self.play(Circumscribe(lobjects[3].all_bell_texts[3].primary_text))
        c = Dot(point=lobjects[3].all_bell_texts[3].get_anchor_position())
        self.play(FadeIn(c, run_time=0.3))
        self.play(MoveAlongPath(c, lobjects[3].bell_lines[4]))
        self.play(FadeOut(c, run_time=0.3))

        placeBells = VGroup()
        for i in range(4):
            t = Text(str(lead_head_positions[i])).next_to(lobjects[i].all_bell_texts[4], direction=RIGHT).scale(0.7)
            c = Circle(color=BLUE).scale(0.25).move_to(t)
            placeBells.add(t, c)
        self.play(Create(placeBells))

        self.play(*[l.unreveal() for l in lobjects], *[Uncreate(p) for p in placeBells])

class paragraph5(Scene):
    def construct(self):
        radius = 2.5
        center = (-2,0,0)
        seconds = Paragraph("Making", "seconds", alignment="center").move_to(center).shift(UP*radius)
        down = Paragraph("3/4", "down", alignment="center").move_to(center).shift(RIGHT*radius)
        fourths = Paragraph("4 blows", "behind", alignment="center").move_to(center).shift(DOWN*radius)
        up = Paragraph("3/4", "up", alignment="center").move_to(center).shift(LEFT*radius)
        texts = [seconds, down, fourths, up]

        arcs = VGroup()
        for i in range(4):
            arcs.add(Arc(angle=-PI/6, start_angle=-PI/6-i*PI/2, radius=radius*1.2).shift(center).add_tip())

        self.play(Write(t) for t in texts)
        self.play(Create(a) for a in arcs)

        #Line
        pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        plain = LineObject(LineGenerator.generate_line([pb])).scale(2.5)
        leDist = plain.ruleoffs[0].get_y()-plain.ruleoffs[1].get_y()
        plain.shift([4,-1.5*leDist,0])
        for i in range(5):
            plain.set_line_visible(i, True)

        #Numbers
        layoutCircle = Circle(radius=radius*0.5).move_to(center)
        anchors = Group(*[Point().move_to(layoutCircle.point_from_proportion(0.25*i)).set_z_index(-1000) for i in range(4)])
        self.add(anchors)
        numbers = [2,3,5,4]
        bell_texts = VGroup(*[BellText(numbers[i], anchors[i]).scale(4).set_color(BELL_COLORS[numbers[i]-2]) for i in range(4)])

        self.add(bell_texts)
        brace = Brace(Group(plain.all_bell_texts[45], plain.all_bell_texts[50]), direction=LEFT)
        self.play(*[Write(b.primary_text) for b in bell_texts], plain.reveal(), FadeIn(brace))

        rotate_texts = [Rotate(b, -PI/2, about_point=center) for b in anchors]
        self.play(*rotate_texts, plain.animate.shift(UP*leDist)) #Do all the rotations
        self.play(*rotate_texts, plain.animate.shift(UP*leDist))
        self.play(*rotate_texts, plain.animate.shift(UP*leDist))
        self.play(*rotate_texts, plain.animate.shift(DOWN*leDist*3))

        lhs = [plain.get_row(i*10) for i in range(5)]
        self.play(FadeIn(lhs[0]), FadeIn(lhs[1]), FadeOut(brace))
        self.play(FadeOut(plain), lhs[0].animate.scale(1.5).set_y(1), lhs[1].animate.scale(1.5).set_y(-1))
        for i in range(2,5):
            lhs[i].scale(1.5).set_y(-1)

        whereEachGoes = [0,3,1,4,2]
        transitionLines = VGroup(*[Line(lhs[0][i].get_bottom(), lhs[1][whereEachGoes[i]].get_top(), buff=0.2) for i in range(5)])

        self.play(Create(transitionLines[0]))
        transitionLineCopies = VGroup()
        #Initial line creation
        for i in range(4):
            c = arcs[[0,3,1,2][i]].copy()
            transitionLineCopies.add(c)
            self.play(c.animate.become(transitionLines[i+1]))
        self.play(*rotate_texts, Indicate(lhs[1]))

        #Up and down thing
        copies = VGroup()
        for i in range(3):
            self.play(FadeOut(copies,run_time=0.1), FadeOut(lhs[i]),lhs[i+1].animate.shift(UP*2))
            copies = VGroup(*[lhs[i+1][j].copy() for j in range(5)])
            self.play(*[copies[j].animate.become(lhs[i+2][whereEachGoes[j]]) for j in range(5)], *rotate_texts)
        self.play(FadeOut(lhs[3]), copies.animate.shift(UP), FadeOut(transitionLines), FadeOut(transitionLineCopies))

        self.play(*[Unwrite(b.primary_text) for b in bell_texts], *[Unwrite(t) for t in texts], *[Uncreate(a) for a in arcs], Unwrite(copies))

class paragraph6(Scene):
    def construct(self):
        pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        plain = LineObject(LineGenerator.generate_line([pb]))
        pbText = Text("One hunt bell:").scale(.5).next_to(plain, direction=UP)
        self.play(plain.reveal())
        self.play(Write(pbText, run_time=1))
        self.play(plain.animate.shift(LEFT*3), pbText.animate.shift(LEFT*3))

        #Banana Doubles
        b = Method(5,"3.125.3,145.3",Calls("","",0,0,1),0,8)
        banana = LineObject(LineGenerator.generate_line([b])).match_height(plain)
        bText = Text("No hunt bell:").scale(.5).next_to(banana, direction=UP)
        self.play(banana.reveal())
        self.play(Write(bText, run_time=1))

        #Banana Doubles
        g = Method(5,"3,1.5.1.5.1",Calls("","",0,0,1),0,10)
        grandsire = LineObject(LineGenerator.generate_line([g])).match_height(plain).shift(RIGHT*3)
        gText = Text("Two hunt bells:").scale(.5).next_to(grandsire, direction=UP)
        self.play(grandsire.reveal())
        self.play(Write(gText, run_time=1))

        self.play(plain.unreveal(), banana.unreveal(), grandsire.unreveal(), *[Unwrite(t) for t in [pbText, bText, gText]])

class paragraph7(Scene):
    def construct(self):
        pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        plain = LineObject(LineGenerator.generate_line([pb])).scale(2.7)
        leDist = plain.ruleoffs[0].get_y()-plain.ruleoffs[1].get_y()
        plain.shift([5,-.5*leDist,0])
        for i in range(5):
            plain.set_line_visible(i, True)
        t = Paragraph("Thanks for watching!", "Created by Matthew Collier", line_spacing=.7)
        t2 = Paragraph("Special thanks to:", "Mick Hutton for letting me borrow his microphone", "Jadd Virji for the support", "All ringers at St. Barnabas", "Everyone in the CUGCR", "", "", "Consider downloading my app \"Campana\" for more ringing fun!", line_spacing=.7).scale(0.5)
        texts = VGroup(t, t2).arrange(direction=DOWN)
        t.to_edge(LEFT).shift(UP)
        t2.to_edge(LEFT).shift(UP)
        campana = ImageMobject("Campana.png").scale(0.6).next_to(t2, direction=DOWN).to_edge(LEFT)
        self.play(FadeIn(plain, run_time=2), Write(texts, run_time=2))
        self.play(FadeIn(campana, run_time=0.5))
        self.wait()

class ammendment(Scene):
    def construct(self):
        #54 seconds
        t = Text("*Without jump changes")
        self.play(Write(t,run_time=0.5))
        self.wait()
        self.play(FadeOut(t))
        self.wait()
        #3:35:57
        t = Paragraph("*If we didn't have the bottom row", "it would be harder to see, for", "example, that a bell is dodging")
        self.play(Write(t,run_time=1))
        self.wait()
        self.play(FadeOut(t))
        self.wait()
        #6:02:22
        t = Paragraph("*There are many other hunt bell", "groups and patterns possible!")
        self.play(Write(t,run_time=1))
        self.wait()
        self.play(FadeOut(t))
        self.wait()
        #38:41
        t = Paragraph("•Starts and ends with rounds", "•No repeated rows", "•Bells can only move a maximum of one position").scale_to_fit_width(config.frame_width * 0.9)
        for l in t:
            self.play(Write(l))
        self.wait()
        self.play(FadeOut(t))
        self.wait()
        #1:09:32
        t = Paragraph("Below: Lead head", "Above: Lead end", "Change: Lead end change").scale_to_fit_width(config.frame_width * 0.9)
        for l in t:
            self.play(Write(l))
        self.wait()
        self.play(FadeOut(t))
        self.wait()
