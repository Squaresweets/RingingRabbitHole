from manim import *
from BellEnd.LineGenerator import LineGenerator as lg
from LineObject import *
from LineObjectGroup import *

pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
pbm = Method(6,"x16x16x16,12",Calls("14","1234",0,12,1),0,12)
cam = Method(6,"x36x14x12x36x14x56,12",Calls("14","1234",0,24,1),0,24)

class paragraph1(Scene):
    def construct(self):
        leadEnds = [[1,2,3,4,5],[1,3,5,2,4],[1,5,4,3,2],[1,4,2,5,3]]
        lobjects = LineObjectGroup(*[LineObject(LineGenerator.generate_line([pb], initial_row=le, lead_end_cap=1))
                    for le in leadEnds])
        lobjects.scale_to_fit_height(config.frame_height * 0.9).center()
        for l in lobjects:
            l.set_line_visible(5, True)
        self.play(lobjects.reveal())
        
        line = lobjects[0]
        self.play(line.animate.center().scale(3), *[FadeOut(lobjects[i]) for i in [1,2,3]])
        self.play(*[line.animate_line_visible(i, True) for i in [2,3,4]])

        g = line.get_all_changes()
        self.play(FadeOut(line), FadeIn(g, run_time=0.1))
        self.play(c.animate.set_y(c.get_y()*1.4) for c in g)
        self.play(c.animate.set_color(WHITE).set_stroke(width=5) for c in g)

        copy = g[9].copy()
        self.play(copy.animate.center().shift(RIGHT*4).scale(1.5))
        t = Text("12345").scale(0.7).next_to(copy, direction=UP)
        for i,n in enumerate(t):
            n.set_x(copy[[0,2,1,4,3][i]].point_from_proportion(0)[0]) #Actually awful lol, im so bad at coding this stuff
        self.play(Write(t))

        notation_text = Text("125").scale(1.2).next_to(copy, direction=DOWN, buff=0.3)
        text_copies = VGroup()
        for i in range(3):
            c = copy[[0,2,3][i]].copy()
            text_copies.add(c)
            self.play(c.animate.become(notation_text[i]))

        long_notation = expand_notation(pb.notation)
        expanded_notation = split_notation(long_notation)
        notation_texts = VGroup()
        for i,n in enumerate(expanded_notation):
            notation_texts.add(Text(n).next_to(g[i], buff=0.5))
        # self.play(Write(notation_texts))
        self.play(text_copies.animate.become(notation_texts[9]), Unwrite(copy), Unwrite(t))
        g_copy = g.copy()
        self.add(g_copy)
        self.play(*[g[i].animate.become(notation_texts[i]) for i in range(9)])
        g[9].become(notation_texts[9])
        self.remove(g, text_copies)
        self.add(notation_texts)

        long_notation_text = Text(long_notation).scale(1.2)
        animations = []
        i=0
        for text in notation_texts:
            for char in text:
                animations.append(char.animate.become(long_notation_text[i]))
                i += 1
            i += 1 #Get around the .

        self.play(*animations, FadeOut(g_copy))
        self.play(FadeIn(long_notation_text))
        self.remove(notation_texts)
        self.play(Unwrite(long_notation_text, run_time=1))

class paragraph2(Scene):
    def construct(self):
        minor_line = LineObject(LineGenerator.generate_line([pbm], lead_end_cap=1)).set_all_lines_visible().scale(2.75).shift(RIGHT*3)
        doubles_line = LineObject(LineGenerator.generate_line([pb], lead_end_cap=1)).set_all_lines_visible().match_height(minor_line).shift(LEFT*3)
        self.play(doubles_line.reveal(), minor_line.reveal())

        doubles = doubles_line.get_all_changes()
        minor = minor_line.get_all_changes()
        self.play(FadeOut(doubles_line), FadeIn(doubles, run_time=0.1), FadeOut(minor_line), FadeIn(minor, run_time=0.1))
        self.play(c.animate.set_y(c.get_y()*1.4).set_color(WHITE).set_stroke(width=5) for c in [*doubles, *minor])

        self.play(Circumscribe(doubles))
        self.play(Circumscribe(minor[i]) for i in range(0,11,2))
        notation = Text(".16..16..16..16..16..12").match_x(minor).shift(LEFT*.5)
        self.play(FadeOut(doubles), minor.animate.match_x(doubles).shift(LEFT), Write(notation, run_time=1))
        self.play(TransformMatchingShapes(notation, Text("x16x16x16x16x16.12").move_to(notation)))

class paragraph3(ThreeDScene):
    def construct(self):
        cm = LineGenerator.generate_line([cam], lead_end_cap=1)
        line = LineObject(cm).set_all_lines_visible().scale_to_fit_height(config.frame_height * 0.9)
        self.play(line.reveal())

        rotated_line = VGroup(l.get_subcurve(0,23/24) for l in line.bell_lines).copy().clear_updaters().set_z_index(-1)
        self.play(rotated_line.animate.shift(RIGHT*3))
        rotation_center = rotated_line.get_center()
        self.play(Rotate(rotated_line, axis=[1,0,0], about_point=rotation_center))
        self.play(rotated_line.copy().animate(remover=True).shift(LEFT*3))

        top_half = VGroup(l.get_subcurve(11/23,1) for l in rotated_line)
        bottom_half = VGroup(l.get_subcurve(0,11/23) for l in rotated_line)
        self.remove(rotated_line)
        self.add(top_half, bottom_half)

        self.play(Rotate(bottom_half, -PI, axis=[1,0,0], about_point=rotation_center))
        self.play(Rotate(bottom_half, PI, axis=[1,0,0], about_point=rotation_center))

        g = line.get_all_changes().scale([1,-1,1])
        g.remove(g[-1])
        g.move_to(rotated_line)
        self.remove(top_half, bottom_half)
        # self.play(c.animate.set_y(c.get_y()*1.4-g.get_y()) for c in g)
        self.play(c.animate.scale(0.75) for c in g)
        self.play(FadeOut(g[i]) for i in range(0,11))

        long_notation = expand_notation(cam.notation)
        expanded_notation = split_notation(long_notation)
        notation_texts = VGroup()
        g2 = line.get_all_changes()
        for i,n in enumerate(expanded_notation):
            notation_texts.add(Text(n).scale(0.5).next_to(g2[i]))

        self.play(*[g[-(i+1)].animate(remover=True).become(notation_texts[i]) for i in range(12)], FadeIn(notation_texts[-1]))

        for i in reversed(range(12, 23)):
            notation_texts.remove(notation_texts[i])
        self.add(notation_texts)

        long_notation_text = Text(cam.notation).scale(1.2)
        animations = []
        i=0
        for text in notation_texts:
            for char in text:
                if cam.notation[i] == ",":
                    i += 1
                animations.append(char.animate.become(long_notation_text[i]))
                i += 1
        
        self.play(*animations, FadeOut(line))
        self.play(FadeIn(long_notation_text))
        self.remove(notation_texts)
        self.play(Circumscribe(long_notation_text[-3]))

        pbd_long_notation = expand_notation(pb.notation)
        self.play(long_notation_text.animate.become(Text(pbd_long_notation)))

        self.play(*[MoveAlongPath(long_notation_text[16-i], ArcBetweenPoints(long_notation_text[16-i].get_center(), long_notation_text[i].get_center(), angle=PI), remover=True) for i in [0,2,4,6]], *[FadeOut(long_notation_text[i]) for i in [9,11,13,15]])
        long_notation_text = VGroup(long_notation_text[i] for i in [0,1,2,3,4,5,6,7,8,17,18,19,20])
        self.play(long_notation_text.animate.become(Text(pb.notation)))
        self.play(Unwrite(long_notation_text))

class paragraph4(ThreeDScene):
    def construct(self):
        notation = Text(pb.notation).scale(1.5).to_edge(UP)
        methods = [Method(i,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10) for i in [5,6,7]]
        lines = Group(*[LineObject(LineGenerator.generate_line([m], lead_end_cap=1)).set_all_lines_visible().scale(3).shift(DOWN*.3) for m in methods]).arrange(buff=1.5)
        self.play(*[l.reveal() for l in lines], Write(notation))

        change_example = lines[0].get_change(9)
        self.play(*[FadeOut(l) for l in lines], change_example.animate.center().scale(3).set_stroke(width=10), notation.animate.become(Text("125").scale(2).shift(UP*2)))
        self.play(Circumscribe(change_example[2]))
        self.play(Circumscribe(change_example[0]))
        self.play(notation.animate.become(Text("25").scale(2).shift(UP*2)))

        self.play(Circumscribe(change_example[0]), Circumscribe(change_example[3]))
        self.play(notation.animate.become(Text("2").scale(2).shift(UP*2)))
        self.play(Circumscribe(change_example[1]))
        self.play(Circumscribe(change_example[0]), Circumscribe(change_example[3]))

        self.play(notation.animate.become(Text("125").scale(2).shift(UP*2)))

