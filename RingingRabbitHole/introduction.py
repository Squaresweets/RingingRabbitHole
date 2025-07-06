from manim import *
from BellEnd.LineGenerator import *
from LineObject import *
from LineObjectGroup import *

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
        t2 = Paragraph("Episode 1:", "The Structure of a Method", alignment="center").scale(0.8).shift(DOWN*3)
        self.play(Write(t2), VGroup(lines, t, name).animate(run_time=0.6).shift(UP*0.8))
        self.wait()
        self.play(self.camera.frame.animate(run_time=0.8, rate_func=smooth).scale(0.005).move_to(t[1][7]))
        # self.play(VGroup(lines, t).animate(rate_func=smoothstep).shift(-t[1][7].get_center()).scale(20))
