from manim import *

class First_scene(Scene):
    def construct(self):
        t = Text("This is the first scene")
        self.play(Write(t))
        self.wait(2)


class Second_scene(Scene):
    def construct(self):
        t = Text("This is the second scene")
        self.play(Write(t))
        self.wait(2)