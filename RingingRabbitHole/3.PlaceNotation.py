
from manim import *
from BellEnd.LineGenerator import LineGenerator as lg
from LineObject import *
from LineObjectGroup import *

pb = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
pbm = Method(6,"x16x16x16,12",Calls("14","1234",0,12,1),0,12)

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
                print(long_notation[i])
                animations.append(char.animate.become(long_notation_text[i]))
                i += 1
            i += 1 #Get around the .

        self.play(*animations, FadeOut(g_copy))
        self.play(FadeIn(long_notation_text))
        self.remove(notation_texts)
        self.play(Unwrite(long_notation_text, run_time=1))
