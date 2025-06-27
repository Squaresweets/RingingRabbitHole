from manim import *
from BellEnd.LineGenerator import *

class First_scene(Scene):
    def construct(self):
        m = Method(5,"5.1.5.1.5,125",Calls("145","123",0,10,1),0,10)
        line = LineGenerator.generate_line([m], Composition(),1)

        table_data = [[str(b) for b in row] for row in line.positions]
        table = Table(table_data, h_buff=0.2, v_buff=0.2)
        table.remove(*table.get_horizontal_lines(), *table.get_vertical_lines())

        table.scale_to_fit_height(config.frame_height * 0.9)
        table.move_to(ORIGIN)
        self.play(Write(table), run_time=1)


class Second_scene(Scene):
    def construct(self):
        t = Text("This is the second scene")
        self.play(Write(t))
        self.wait(2)
