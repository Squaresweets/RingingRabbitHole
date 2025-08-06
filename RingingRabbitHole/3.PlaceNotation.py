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
        new_notation = Text("x16x16x16x16x16.12").move_to(notation)
        self.play(TransformMatchingShapes(notation, new_notation))

        self.play(Unwrite(new_notation, run_time=1), Unwrite(minor, run_time=1))

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
        
        external_only = LineObject(MethodLine([[1,2,3,4,5,6],[1,3,2,5,4,6]], "", 6, [], [])).set_all_lines_visible().scale(9)
        for j in external_only.bell_lines:
            j.set_stroke(width=10)

        self.play(change_example.animate.become(VGroup(*external_only.bell_lines)), notation.animate.become(Text("16  or  1  or  6").scale(2).shift(UP*2)))

        self.play(Unwrite(notation, run_time=1), Unwrite(change_example, run_time=1))
        

class paragraph5(Scene):
    def construct(self):
        line = LineObject(LineGenerator.generate_line([pb], lead_end_cap=1)).set_all_lines_visible().scale_to_fit_height(config.frame_height * 0.9)

        expanded_notation = split_notation(expand_notation(pb.notation))
        notation_texts = VGroup()
        g = line.get_all_changes()
        for i,n in enumerate(expanded_notation):
            notation_texts.add(Text(n).set_opacity(0.5).next_to(g[i], direction=LEFT, buff=.4))
        self.play(line.reveal(), Write(notation_texts))

        for i in range(2):
            call_line = lg.generate_line([pb], Composition(5, [CompositionPart(["b","s"][i])]), 1)
            self.play(line.animate_to_new_composition(call_line), notation_texts[9].animate.become(Text(["145","123"][i], fill_opacity=.5).set_color(RED), match_center=True))

        j = Method(5,"(42).[321].5.1.5.1.5.1.5.125",Calls("145","123",0,10,1),0,10)
        jump = lg.generate_line([j], lead_end_cap=1)
        self.play(line.animate_to_new_composition(jump),
                  notation_texts[0].animate.become(Text("(42)").set_opacity(0.5).next_to(g[0], direction=LEFT, buff=.4)),
                  notation_texts[1].animate.become(Text("[321]").set_opacity(0.5).next_to(g[1], direction=LEFT, buff=.4)),
                  notation_texts[9].animate.become(Text("125").set_opacity(0.5).next_to(g[9], direction=LEFT, buff=.4)))
        Text(n).set_opacity(0.5).next_to(g[i], direction=LEFT, buff=.4)

        self.play(Unwrite(notation_texts, run_time=1), line.unreveal())

class paragraph6(Scene):
    def construct(self):
        notation = Text("x16x16x16,12")
        self.play(Write(notation, run_time=1))
        self.play(notation.animate.become(Text("a &-16-16-16,+12")))
        self.play(Circumscribe(notation[0]))
        self.play(Circumscribe(VGroup(notation[1],notation[10])))
        self.play(Circumscribe(VGroup(notation[12],notation[14])))
        self.play(FadeOut(notation[11]))
        notation.remove(notation[11])
        self.play(Unwrite(notation))

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

class introduction(MovingCameraScene):
    def construct(self):
        pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        plain = LineObject(LineGenerator.generate_line([pb]))
        for i in range(5):
            plain.set_line_visible(i, True)
        
        lines = VGroup(plain.bell_lines).clear_updaters()
        self.play(Create(l, rate_func=smoothstep, run_time=1) for l in lines)
        radius = 2.5
        height = lines.height
        def bend(p):
            x, y, z = p
            angle = y/(height/2)*PI+PI/2
            return (radius+x) * np.array([np.sin(angle), -np.cos(angle), 0])
        self.play(ApplyPointwiseFunction(bend, lines, run_time=2))

        t = Paragraph("The Ringing", "Rabbit Hole", alignment="center")
        name = Text("By Matthew Collier").scale(0.5).next_to(t,direction=DOWN)
        self.play(Write(VGroup(t,name)))
        t2 = Paragraph("Episode 3:", "Place Notation", alignment="center").scale(0.8).shift(DOWN*3)
        self.play(Write(t2), VGroup(lines, t, name).animate(run_time=0.6).shift(UP*0.8))
        self.wait()
        self.play(self.camera.frame.animate(run_time=0.8, rate_func=smooth).scale(0.005).move_to(t[1][7]))
        # self.play(VGroup(lines, t).animate(rate_func=smoothstep).shift(-t[1][7].get_center()).scale(20))
