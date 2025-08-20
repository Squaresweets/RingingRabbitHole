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
    return VGroup(*m, *arrows)

def arrange_into_line(m, buff=1):
    center = m.get_center()
    for i, item in enumerate(m):
        item.set_y(center[1]).set_x(center[0]+buff*(i-(len(m)-1)/2))

def Rotate_no_spin(mobject, angle, about_point=ORIGIN):
    start_pos = mobject.get_center()
    def update(mob, alpha):
        theta = angle * alpha
        rot_matrix = rotation_matrix(theta, OUT)  # 2D rotation in XY plane
        offset = start_pos - about_point
        new_pos = about_point + rot_matrix @ offset
        mob.move_to(new_pos)
    return UpdateFromAlphaFunc(mobject, update)

def Rotate_co(m):
    co = sorted(m.submobjects, key=lambda x: x.get_center()[0])
    return AnimationGroup(*[co[i].animate.move_to(co[i+1]) for i in range(len(co)-1)], MoveAlongPath(co[-1], ArcBetweenPoints(co[-1].get_center(), co[0].get_center(), angle=PI)))

class test(Scene):
    def construct(self):
        order = [4,6,8,7,5,3,2]
        placeBells = arrange_into_circle([Text(str(i), color = BELL_COLORS[i-1]) for i in order], ORIGIN, 3, add_arrows=True)
        bells = arrange_into_circle([Text(str(i)) for i in order], ORIGIN, 2)
        self.play(Write(placeBells), Write(bells))
        rotate_texts = [Rotate_no_spin(b, -2*PI/7, ORIGIN) for b in bells]
        # self.play(*rotate_texts)
        
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

        leading_order_example = Text("24687531").scale(0.9)
        arrange_into_line(leading_order_example, 0.4)
        leading_order_example.next_to(line, direction=LEFT, buff=1)
        for i in range(8):
            self.play(VGroup(line.all_bell_texts[8+16*i].copy().clear_updaters(),
                             line.all_bell_texts[16+16*i].copy().clear_updaters())
                      .animate.become(leading_order_example[i]))
        self.play(line.animate_line_visible(i, True) for i in [2,4,6])
        self.play(*[line.animate_line_visible(i, False) for i in [2,4,6,8]],
                  *[line.animate_line_visible(i, True) for i in [3,5,7]])
        self.play(*[line.animate_line_visible(i, False) for i in [3,5,7]],
                  line.animate_line_visible(8, True))