from manim import *
from BellEnd.LineGenerator import LineGenerator as lg
from LineObject import *
from LineObjectGroup import *

pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
# pbm = Method(6,"x16x16x16,12",Calls("14","1234",0,12,1),0,12)
pbm = Method(8, "x18x18x18x18,12",Calls("14","1234",0,16,1),0,16)
cam = Method(6,"x36x14x12x36x14x56,12",Calls("14","1234",0,24,1),0,24)

def arrange_into_circle(m, center, radius, angle_offset=0, add_arrows = False):
    num = len(m)
    for i, item in enumerate(m):
        angle = -2 * PI * i / num + PI/2 + angle_offset
        item.move_to(center + radius * np.array([np.cos(angle), np.sin(angle), 0]))
    if not add_arrows:
        return VGroup(*m)
    buff = 0.3
    angle = 2*PI/num # Ignoring the buffer
    arrows = [Arc(angle=-(angle - buff*2), start_angle=PI/2 - i*angle - buff, radius=radius).shift(center).add_tip() for i in range(num)]
    return VGroup([x for pair in zip(m, arrows) for x in pair]) #Interleaved so arrows are between

def arrange_into_line(m, buff=1):
    center = m.get_center()
    for i, item in enumerate(m):
        item.set_y(center[1]).set_x(center[0]+buff*(i-(len(m)-1)/2))
    return m

def Rotate_no_spin(mobject, angle, about_point=ORIGIN, scale=1):
    start_pos = mobject.get_center()
    def update(mob, alpha):
        theta = angle * alpha
        rot_matrix = rotation_matrix(theta, OUT)  # 2D rotation in XY plane
        offset = start_pos - about_point
        new_pos = about_point + rot_matrix @ offset * (1 + (scale - 1) * alpha)
        mob.move_to(new_pos)
    return UpdateFromAlphaFunc(mobject, update)

def Rotate_co(m, run_time=1, reverse=False):
    co = sorted(m.submobjects, key=lambda x: x.get_center()[0])
    if reverse:
        return AnimationGroup(*[co[i].animate.move_to(co[i-1]) for i in range(1,len(co))], MoveAlongPath(co[0], ArcBetweenPoints(co[0].get_center(), co[-1].get_center(), angle=-PI)), run_time = run_time)
    else:
        return AnimationGroup(*[co[i].animate.move_to(co[i+1]) for i in range(len(co)-1)], MoveAlongPath(co[-1], ArcBetweenPoints(co[-1].get_center(), co[0].get_center(), angle=PI)), run_time = run_time)

def create_transposition(t, include_straight_lines = False, add_updaters = False):
    output = VGroup()
    output.add(VGroup(Dot().scale(0.6) for _ in range(len(t))).arrange(buff=0.3))
    output.add(VGroup(Dot().scale(0.6) for _ in range(len(t))).arrange(buff=0.3).shift(DOWN*0.5)) # Bottom row
    def make_line_updater(start, end):
        def update_line(l):
            l.set_points_by_ends(start.get_bottom(), end.get_top(), buff=0.03)
        return update_line
    for i,n in enumerate(t):
        if i == n and not include_straight_lines:
            continue
        output.add(Line(output[0][i].get_bottom(), output[1][n].get_top(), buff=0.03))
        if add_updaters:
            output[-1].add_updater(make_line_updater(output[0][i], output[1][n]))
    return output

class test(Scene):
    def construct(self):
        order = [4,6,8,7,5,3,2]
        placeBells = arrange_into_circle([Text(str(i), color = BELL_COLORS[i-1]) for i in order], ORIGIN, 3, add_arrows=True)
        bells = arrange_into_circle([Text(str(i)) for i in order], ORIGIN, 2)
        self.play(Write(placeBells), Write(bells))
        rotate_texts = [Rotate_no_spin(b, -2*PI/7, ORIGIN) for b in bells]
        self.play(*rotate_texts)
        
        co = Text("7532468").arrange(buff=0.3)
        self.play(TransformMatchingShapes(bells, co))
        self.play(MoveAlongPath(co[6], ArcBetweenPoints(co[6].get_center(), co[0].get_center(), angle=PI)), *[co[i].animate.shift(RIGHT*0.6) for i in range(6)])

class paragraph1(Scene):
    def construct(self):
        co = Text("75312468").scale(2)
        arrange_into_line(co)
        self.play(Write(co))
        self.play(Circumscribe(VGroup(co[0], co[3])))
        self.play(Circumscribe(VGroup(co[4], co[7])))
        self.play(Rotate_co(co))
        self.play(Rotate_co(co))
        
        co2 = Text("75312468").scale(2).set_opacity(0)
        arrange_into_line(co2)
        self.play(co2.animate.set_opacity(1).shift(DOWN*1.5))

        coText = Text("Coursing order:").scale(2.3).shift(UP*2)
        self.play(Write(coText))
        self.play(Unwrite(coText, run_time=0.7), Unwrite(co, run_time=0.7), co2.animate.scale(0.4).to_corner(UR))

class paragraph2(Scene):
    def construct(self):
        trText = Text("75312468").scale(0.8) #Boiler plate stuff to keep this text in top right
        arrange_into_line(trText, 0.4)
        self.add(trText.to_corner(UR))

        line = LineObject(LineGenerator.generate_line([pbm], lead_end_cap=1)).set_line_visible(8, True).scale(3)
        self.play(line.reveal())

        # First column animation
        first_column = VGroup(line.all_bell_texts[i*line.stage].primary_text.copy().set_opacity(1) for i in range(1,17))
        self.play(FadeIn(first_column))
        self.play(first_column.animate.shift(LEFT*3))
        center = first_column.get_center() # Will be used later
        distance = first_column[0].get_y()-first_column[1].get_y()
        self.play(first_column[i].animate(remover=True).shift(UP*distance) for i in range(1, 16, 2))
        self.play(Rotate_no_spin(first_column[i], PI/2, center, scale=0.5) for i in range(0, 16, 2))
        self.play(FadeOut(first_column[i]) for i in range(0, 16, 2))

        followed_positions = list(range(8,8*8,9)) + list(range(70,119,7))
        followed = VGroup(line.all_bell_texts[i].primary_text.copy().set_opacity(1) for i in followed_positions)
        self.play(FadeIn(followed))
        self.play(Indicate(f) for f in followed)
        self.play(f.animate.set_x(center[0]) for f in followed)

        first_half = VGroup(followed[i] for i in range(7))
        second_half = VGroup(followed[i] for i in range(7,14))
        self.play(*[Rotate_no_spin(f, PI/2, first_half.get_center()) for f in first_half],
                  *[Rotate_no_spin(f, PI/2, second_half.get_center()) for f in second_half])
        self.play(FadeOut(second_half))

        new_1 = line.all_bell_texts[0].primary_text.copy().set_opacity(1) #Just to ensure it is the right size
        new_1.set_y(first_half.get_y()).set_x(first_half[6].get_x()+distance) # Goofy ahh code
        self.play(FadeIn(new_1))
        first_half.add(new_1)

        for _ in range(4): # Rotate so 8 is at the back
            self.play(Rotate_co(first_half, 0.5))
        self.play(FadeOut(first_half[3]))
        first_half.remove(first_half[3])
        self.play(*[Rotate_no_spin(f, -PI/2, first_half.get_center()) for f in first_half])

        followed_positions = list(range(6,50,7))
        followed = VGroup(line.all_bell_texts[i].primary_text.copy().set_opacity(1) for i in followed_positions)
        self.play(TransformMatchingShapes(first_half, followed))
        self.play(FadeOut(followed))

        self.play(line.animate_line_visible(6, True))
        self.play(line.animate_line_visible(7, True))
        self.play(Circumscribe(trText[6]))
        self.play(Circumscribe(trText[0]))
        self.play(line.animate_line_visible(6, False), line.animate_line_visible(7, False))

class paragraph3(Scene):
    def construct(self):
        trText = Text("75312468").scale(0.8) #Boiler plate stuff to keep this text in top right
        arrange_into_line(trText, 0.4)
        self.add(trText.to_corner(UR))
        old_line = LineObject(LineGenerator.generate_line([pbm], lead_end_cap=1)).set_line_visible(8, True).scale(3)
        self.add(old_line)
        line = LineObject(LineGenerator.generate_line([pbm], lead_end_cap=2)).set_line_visible(8, True).scale(3)
        line.shift(old_line.anchors[0].get_center() - line.anchors[0].get_center()) #match up position with 2 leads
        self.play(FadeIn(line))
        self.remove(old_line)

        self.play(line.anchors.animate.shift(LEFT*4.5), trText.animate.scale(0.7).to_corner(UR).set_opacity(0.7))

        order = [4,6,8,7,5,3,2]
        center_of_circle = RIGHT*2
        placeBells = arrange_into_circle([Text(str(i), color = BELL_COLORS[i-1]) for i in order], center_of_circle, 3, add_arrows=True)
        bells = arrange_into_circle([Text(str(i)) for i in order], center_of_circle, 2)
        self.play(Write(placeBells, run_time=1), Write(bells, run_time=1))
        def rotate_texts(angle = 2*PI/7):
            return [Rotate_no_spin(b, -angle, center_of_circle) for b in bells]

        self.play(*rotate_texts())
        
        # Example, 5 doing 3s work
        self.play(Circumscribe(bells[4]))
        self.play(Circumscribe(placeBells[10]))
        self.play(rotate_texts(-2*PI/7))

        row_distance = line.anchors[0].get_center()[1] - line.anchors[8].get_center()[1]
        lead_distance = row_distance * 16
        line_frame = SurroundingRectangle(VGroup(line.all_bell_texts[8], line.all_bell_texts[16]))
        placeBell_frame = SurroundingRectangle(bells[6])
        self.play(Create(line_frame))
        self.play(Create(placeBell_frame))
        self.play(rotate_texts(), line.anchors.animate.shift(UP*lead_distance))

        for _ in range(6):  
            self.play(line_frame.animate.shift(DOWN*row_distance*2), Rotate_no_spin(placeBell_frame, -2*PI/7, center_of_circle))
        self.play(Uncreate(line_frame), Uncreate(placeBell_frame))

        co = Text("7532468").arrange(buff=0.3).shift(center_of_circle)
        self.play(FadeOut(placeBells), TransformMatchingShapes(bells, co), trText.animate.scale(1/0.7).to_corner(UR).set_opacity(1))
        self.play(line.anchors.animate.shift(DOWN*lead_distance))
        self.play(co.animate.become(Text("75312468").arrange(buff=0.3).shift(center_of_circle)))
        one = co[3]
        co.remove(one)
        self.add(one)
        self.play(Rotate_co(co), line.anchors.animate.shift(UP*lead_distance))
        self.play(Rotate_co(co, reverse=True), FadeOut(line))

        co.add(one)
        self.play(co.animate.center())

class paragraph4(Scene):
    def construct(self):
        co = Text("75312468").arrange(buff=0.3)
        trText = Text("75312468").scale(0.8) #Boiler plate stuff to keep this text in top right
        arrange_into_line(trText, 0.4)
        self.add(trText.to_corner(UR), co)
        one = co[3]
        co.remove(one)
        self.play(co.animate.arrange(buff=0.3), one.animate.shift(DOWN*0.8).set_opacity(0.5))
        self.play(one.animate.shift(LEFT*1.2))
        self.play(one.animate.shift(RIGHT*0.6*5))
        self.play(FadeOut(one))
        self.play(Indicate(co[6]))
        
        self.play(FadeOut(co[i]) for i in [0,6])
        co.remove(co[0], co[6])

        order = [4,6,8,7,5,3,2]
        center_of_circle = ORIGIN
        placeBells = arrange_into_circle([Text(str(i), color = BELL_COLORS[i-1]) for i in order], center_of_circle, 3, add_arrows=True)
        bells = arrange_into_circle([Text(str(i)) for i in order], center_of_circle, 2)
        def rotate_texts(angle = 2*PI/7):
            return [Rotate_no_spin(b, -angle, center_of_circle) for b in bells]
        
        self.play(Write(placeBells, run_time=1), TransformMatchingShapes(co, bells))
        self.play(bells[2].animate.set_opacity(0.2), bells[3].animate.set_opacity(0.2))
        co = Text("53246").arrange(buff=0.3).next_to(placeBells, buff=0.5)
        important_bells = VGroup(bells[i] for i in [4,5,6,0,1])
        self.play(TransformMatchingShapes(important_bells.copy(), co))
        for _ in range(4):
            self.play(rotate_texts())
            self.play(TransformMatchingShapes(important_bells.copy(), co))
        self.play(FadeOut(co))

        one = Text("1").set_color(RED).shift([-2,.5,0])
        self.play(Write(one))
        important_bells.add(one)

        #Horrible code but works
        co = Text("532461").arrange(buff=0.3).scale(0.8).next_to(placeBells, buff=0.5)
        self.play(TransformMatchingShapes(important_bells.copy(), co))
        self.play(rotate_texts())
        co2 = Text("532416").arrange(buff=0.3).scale(0.8).next_to(co, direction=DOWN)
        self.play(TransformMatchingShapes(important_bells.copy(), co2))
        self.play(rotate_texts())
        co3 = Text("532146").arrange(buff=0.3).scale(0.8).next_to(co2, direction=DOWN)
        self.play(TransformMatchingShapes(important_bells.copy(), co3))
        self.play(rotate_texts())
        co4 = Text("531246").arrange(buff=0.3).scale(0.8).next_to(co3, direction=DOWN)
        self.play(TransformMatchingShapes(important_bells.copy(), co4))

        self.play(FadeOut(VGroup(co, co2, co3, co4)), bells[2].animate.set_opacity(1), bells[3].animate.set_opacity(1))
        
        important_bells.add(bells[6]).add(bells[2], bells[3])
        co = Text("12468753").arrange(buff=0.3).scale(0.6).next_to(placeBells, buff=0.5)
        self.play(TransformMatchingShapes(important_bells.copy(), co))
        self.play(rotate_texts())
        co2 = Text("13246875").arrange(buff=0.3).scale(0.6).next_to(co, direction=DOWN)
        self.play(TransformMatchingShapes(important_bells.copy(), co2))
        self.play(rotate_texts())
        co3 = Text("15324687").arrange(buff=0.3).scale(0.6).next_to(co2, direction=DOWN)
        self.play(TransformMatchingShapes(important_bells.copy(), co3))
        self.play(rotate_texts())
        co4 = Text("17532468").arrange(buff=0.3).scale(0.6).next_to(co3, direction=DOWN)
        self.play(TransformMatchingShapes(important_bells.copy(), co4))

        self.play(FadeOut(VGroup(co, co2, co3, co4, one)))

class paragraph5(Scene):
    def construct(self):
        trText = Text("75312468").scale(0.8) #Boiler plate stuff to keep this text in top right
        arrange_into_line(trText, 0.4)
        self.add(trText.to_corner(UR))

        order = [4,6,8,7,5,3,2]
        center_of_circle = ORIGIN

        placeBells = arrange_into_circle([Text(str(i), color = BELL_COLORS[i-1]) for i in order], center_of_circle, 3, add_arrows=True)
        bells = arrange_into_circle([Text(str(i)) for i in [5,3,2,4,6,8,7]], center_of_circle, 2)

        one = Text("1").set_color(RED).shift([-2,.5,0])
        self.add(placeBells, bells)

        def rotate_texts(rotations = 1):
            for _ in range(rotations):
                temp = bells[6] #Rotate around the bells in the array
                bells.remove(temp)
                bells.insert(0, temp)
            return [Rotate_no_spin(b, -2*PI/7 * rotations, center_of_circle) for b in bells]
        def bob_rotate():
            animations = [bells[4].animate.move_to(bells[0])] + [Rotate_no_spin(bells[i], -2*PI/7, center_of_circle) for i in range(4)]
            temp = bells[4]
            bells.remove(temp)
            bells.insert(0, temp)
            return animations
        
        self.play(rotate_texts(4))
        self.play(Circumscribe(VGroup(placeBells[8], bells[4])),
                  Circumscribe(VGroup(placeBells[10], bells[5])),
                  Circumscribe(VGroup(placeBells[12], bells[6])))


        important_bells = VGroup(bells[i] for i in [0,1,4,5,6])
        co = Text("53246").arrange(buff=0.3).next_to(placeBells, buff=0.5).shift(UP*.5)
        self.play(TransformMatchingShapes(important_bells.copy(), co), bells[2].animate.set_opacity(0.2), bells[3].animate.set_opacity(0.2))

        self.play(bob_rotate())

        co2 = Text("32546").arrange(buff=0.3).next_to(co, direction=DOWN, buff=1)
        self.play(TransformMatchingShapes(important_bells.copy(), co2))

        transitionLines = VGroup(*[Line(co[i].get_bottom(), co2[[2,0,1][i]].get_top(), buff=0.2) for i in range(3)])
        self.play(Create(transitionLines))

        remembering = Paragraph("Remembering:", "Tenors PB:", "7", alignment="center").scale(0.7).shift(LEFT*5)
        remembering[2][0].set_color(BELL_COLORS[6])
        self.play(Write(remembering, run_time=1))

        new_bells = arrange_into_circle([Text(str(i)) for i in [8,7,5,3,2,4,6]], center_of_circle, 2)
        new_bells[0].set_opacity(0.2)
        new_bells[1].set_opacity(0.2)
        # self.play(TransformMatchingShapes(bells, new_bells), remembering[2][0].animate.become(Text("4").set_color(BELL_COLORS[3]), match_center=True))
        self.play(bells.animate.become(new_bells), remembering[2][0].animate.become(Text("4").set_color(BELL_COLORS[3]), match_center=True))

        ball = Dot(bells[1].get_center()*0.7, radius=0.1)
        arrow = Arrow(start=.2*UP, end=.2*DOWN).next_to(co[0], direction=UP, buff=0.1).shift(LEFT*0.6)
        self.play(FadeIn(ball), FadeIn(arrow))

        # Bouncing ball animation
        ball_copies = VGroup()
        arrow_copies = VGroup()
        for i in range(2,7):
            start = ball.get_center()
            end = bells[i].get_center() * 0.7
            arc = ArcBetweenPoints(
                start, end,
                angle=PI/3 
            )
            self.play(MoveAlongPath(ball, arc), arrow.animate.shift(RIGHT*0.6), run_time=0.6)
            if i > 3:
                ball_copies.add(ball.copy())
                arrow_copies.add(arrow.copy())
                self.add(arrow_copies[-1], ball_copies[-1])
            self.wait(0.2)
        self.play(transitionLines.animate.shift(0.6*2*RIGHT), co2.animate.become(Text("53624").arrange(buff=0.3), match_center=True))
        self.remove(ball, arrow)

        for i in range(2):
            self.play(rotate_texts(), transitionLines.animate.shift(LEFT*0.6), arrow_copies.animate.shift(LEFT*0.6), remembering[2][0].animate.become(Text(["6","8"][i]).set_color(BELL_COLORS[[5,7][i]]), match_center=True), co2.animate.become(Text(["52436","32546"][i]).arrange(buff=0.3), match_center=True))

        self.play(FadeOut(arrow_copies, ball_copies))

        new_placeBells = arrange_into_circle([Text(["In", "Before", "Middle", "Fourths", "Home", "Fifths", "Wrong"][i-2], color = BELL_COLORS[i-1]).scale(0.5) for i in order], center_of_circle, 3, add_arrows=True)
        self.play(placeBells.animate.become(new_placeBells), remembering[2][0].animate.become(Text("Wrong").scale(0.5).set_color(BELL_COLORS[7]), match_center=True))

        tenors_together = [0,2,4,10]
        other = [1,3,5,6,7,8,9,11,12,13]
        bob_transpositions = [[0,1,4,2,3],[0,3,1,2,4],[2,0,1,3,4],[1,2,3,4,0]]
        single_transpositions = [[0,1,4,3,2],[0,3,2,1,4],[2,1,0,3,4],[1,2,3,4,0,6,5]]
        call_table = MobjectTable([[Text("Position:"), Text("Bob:"), Text("Single:")],
                                    *[[placeBells[n].copy().scale(2), create_transposition(bob_transpositions[i]), create_transposition(single_transpositions[i])] for i,n in enumerate(tenors_together)]])
        call_table.scale_to_fit_height(config.frame_height*0.9)
        new_trText = Text("53246 87").scale(0.8*0.7).set_opacity(0.7)
        arrange_into_line(new_trText, 0.4).to_corner(UR, buff=0.2)
        self.play(FadeOut(remembering, bells, *[placeBells[i] for i in other], co, co2),
                  *[placeBells[tenors_together[i]].animate.become(call_table.get_entries((i+2,1))) for i in range(4)],
                  transitionLines.animate.become(VGroup(call_table.get_entries((4,2))[i] for i in [2,3,4])),
                  trText.animate.become(new_trText))
        self.play(FadeIn(call_table))

        bob_before_entry = call_table.get_entries((5,2))
        n_bob_before = create_transposition([0,1,2,3,6,4,5], True, True).move_to(bob_before_entry)
        single_before_entry = call_table.get_entries((5,3))
        n_single_before = create_transposition([0,1,2,3,6,5,4], True, True).move_to(single_before_entry)
        self.play(FadeOut(bob_before_entry, single_before_entry), FadeIn(n_bob_before, n_single_before))
        self.play(Rotate_co(n_bob_before[1]), Rotate_co(n_single_before[1]))

        #Horrible code
        self.play(FadeOut(n_bob_before[0][5], n_bob_before[0][6], n_bob_before[1][4], n_bob_before[1][5], n_bob_before[7], n_bob_before[8]),
                  VGroup(*[n_bob_before[0][i] for i in range(5)], *[n_bob_before[1][i] for i in [0,1,2,3,6]]).animate.shift(RIGHT*0.45))