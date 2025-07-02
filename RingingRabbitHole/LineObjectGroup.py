from manim import *
from LineObject import *

class LineObjectGroup(Group):
    def __init__(self, *lines):
        super().__init__(*lines)
        self.arrange_vertically()
    
    def arrange_vertically(self):
        for m1, m2 in zip(self.submobjects, self.submobjects[1:]):
            m2.shift(m1.get_bottom_left_pos() - m2.get_top_left_pos())
        return self.center()
    
    def arrange_horizontally(self):
        return super().arrange(direction=RIGHT, buff=0.5)

    def reveal(self, animate_together=True):
        if animate_together:
            all_bell_texts = VGroup(t for s in self.submobjects for t in s.all_bell_texts)
            all_bell_lines = VGroup(*[
                VGroup(*group) for group in zip(*(s.bell_lines for s in self.submobjects))
            ])
            all_ruleoffs = VGroup(t for s in self.submobjects for t in s.ruleoffs)
            sequence = [Write(all_bell_texts, rate_func=smoothstep, run_time=1),
                        *[Create(l, rate_func=smoothstep, run_time=1) for l in all_bell_lines],
                        *[Create(l, rate_func=smoothstep, run_time=1) for l in all_ruleoffs]]
            return AnimationGroup(*sequence, lag_ratio=0)
        else:
            return AnimationGroup(s.reveal() for s in self.submobjects)
    
    def unreveal(self, animate_together=True):
        if animate_together:
            all_bell_texts = VGroup(t for s in self.submobjects for t in s.all_bell_texts)
            all_bell_lines = VGroup(*[
                VGroup(*group) for group in zip(*(s.bell_lines for s in self.submobjects))
            ])
            all_ruleoffs = VGroup(t for s in self.submobjects for t in s.ruleoffs)
            sequence = [Unwrite(all_bell_texts, rate_func=smoothstep, run_time=1),
                        *[Uncreate(l, rate_func=smoothstep, run_time=1) for l in all_bell_lines],
                        *[Uncreate(l, rate_func=smoothstep, run_time=1) for l in all_ruleoffs]]
            return AnimationGroup(*sequence, lag_ratio=0)
        else:
            return AnimationGroup(s.unreveal() for s in self.submobjects)
    
    def animate_line_visible(self, bell, visible):
        return AnimationGroup(l.animate_line_visible(bell, visible) for l in self.submobjects)
    # Can add more as needed