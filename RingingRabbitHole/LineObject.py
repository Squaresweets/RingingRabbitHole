from manim import *
from BellEnd.LineGenerator import *
from BellEnd.Helper import *

BELL_COLORS = ['#4073EE', '#48DD00', '#D511E0', '#DCDD00', '#4DDDDE', '#386754', '#AA7700', '#EE5B56', '#756BFF', '#185BE1', '#009018', '#F100FF', '#FEFF00', '#00FFB1', '#083321', '#FFB200', '#FF0800', '#8E86FF', '#3500FF', '#FFFFFF']
HUNT_BELL_COLOR = "#FF3636"
GRID_SPACING = 0.15

class LineObject(Mobject):
    def __init__(self, line):
        self.line = line
        super().__init__()

        #Create all the dummy objects that we use as anchors and stuff
        self.table_data = [bell_value_to_string[b] for row in line.positions for b in row]
        self.table = Group()
        self.table.add(*[Point().set_z_index(-1000) for _ in self.table_data]) #Create dummy objects for all the positions
        self.table.arrange_in_grid(cols=self.line.stage, buff=GRID_SPACING)
        self.add(self.table)

        def tie_position_to(target, offset=ORIGIN): #TODO: Extract out this weird scaling stuff
            return lambda m : m.move_to(target).shift(offset * (self.table[1].get_center()[0]-self.table[0].get_center()[0])/GRID_SPACING)
        #Put the actual text in, tied to the position of the dummies
        self.bell_texts = VGroup()
        for i in range(len(self.table_data)):
            t = Text(self.table_data[i], font_size=10)
            t.add_updater(tie_position_to(self.table[i])) #used for iteration stuff
            t.update()
            self.add(t)
            self.bell_texts.add(t)

        #Add in the ruleoffs
        self.ruleoffs = VGroup()
        self.add(self.ruleoffs)
        def make_ruleoff_updater(h):
            def ruleoff_updater(mob):
                positions = [(self.get_bell_dummy_entry((h,0)).get_center() +
                              self.get_bell_dummy_entry((h+1,0)).get_center())/2,
                             (self.get_bell_dummy_entry((h,self.line.stage-1)).get_center() +
                              self.get_bell_dummy_entry((h+1,self.line.stage-1)).get_center())/2]
                mob.set_points_as_corners(positions)
            return ruleoff_updater
        for h in self.line.ruleoffs:
            if h > len(self.line.positions) or h < 0:
                continue
            p = VMobject(stroke_opacity=0.7)
            p.add_updater(make_ruleoff_updater(h))
            p.update()
            self.ruleoffs.add(p)
        
        # Create all the bell lines
        self.bell_lines = [VMobject() for _ in range(line.stage)]
        bell_color_index = 0
        def make_line_updater(b_val):
            def line_updater(mob):
                positions = [g.get_center() for g in self.get_bell_dummy_entries(b_val + 1)]
                mob.set_points_as_corners(positions)
            return line_updater
        for b in range(line.stage):
            l = self.bell_lines[b]

            l.add_updater(make_line_updater(b))
            l.update()

            if b+1 in line.huntBells:
                l.set_color(HUNT_BELL_COLOR)
                l.stroke_width = 2
                self.set_bell_visible(b+1, False) # make it visible
            else:
                l.set_color(BELL_COLORS[bell_color_index])
                bell_color_index += 1
                l.stroke_width = 5
                l.set_opacity(False) # make it invisible

            self.add(self.bell_lines[b])

    def get_bell_text_entry(self, pos): #Returns the TEXT
        return self.bell_texts[pos[1]+pos[0]*self.line.stage]
    
    def get_bell_text_entries(self, bell):
        return [self.get_bell_text_entry((i,row[bell])) for i,row in enumerate(self.line.indexes)]

    def get_bell_dummy_entry(self, pos): #Returns the TEXT
        return self.table[pos[1]+pos[0]*self.line.stage]
    
    def get_bell_dummy_entries(self, bell):
        return [self.get_bell_dummy_entry((i,row[bell])) for i,row in enumerate(self.line.indexes)]
    
    def set_bell_visible(self, bell, visible):
        bellEntries = self.get_bell_text_entries(bell)
        for e in bellEntries:
            e.set_opacity(visible)
    
    def set_line_visible(self, bell, visible, also_change_numbers=True):
        self.bell_lines[bell-1].set_opacity(visible)
        self.bell_lines[bell-1].set_fill(opacity=0)
        if also_change_numbers:
            self.set_bell_visible(bell, not visible)
    
    def animate_line_visible(self, bell, visible):
        if visible:
            self.set_line_visible(bell, True, False)
            sequence = [Create(self.bell_lines[bell-1], rate_func=smoothstep, run_time=1),
                    AnimationGroup(*[Unwrite(l) for l in self.get_bell_text_entries(bell)], lag_ratio=0.1, run_time=1)]
        else:
            self.set_bell_visible(bell, True)
            sequence = [Uncreate(self.bell_lines[bell-1],rate_func=smoothstep, run_time=1),
                    AnimationGroup(*[Write(l) for l in reversed(self.get_bell_text_entries(bell))], lag_ratio=0.1, run_time=1)]

        return Succession(AnimationGroup(*sequence, lag_ratio=0),
                            UpdateFromFunc(None, lambda m: self.set_line_visible(bell, visible), run_time=0))
    
    def reveal(self):
        sequence = [Write(self.bell_texts, rate_func=smoothstep, run_time=1),
                    *[Create(l, rate_func=smoothstep, run_time=1) for l in self.bell_lines],
                    *[Create(l, rate_func=smoothstep, run_time=1) for l in self.ruleoffs]]
                    # *[Write(self.get_horizontal_lines())]]
        return AnimationGroup(*sequence, lag_ratio=0)

    def unreveal(self):
        sequence = [Unwrite(self.bell_texts, rate_func=smoothstep, run_time=1),
                    *[Uncreate(l, rate_func=smoothstep, run_time=1) for l in self.bell_lines],
                    *[Uncreate(l, rate_func=smoothstep, run_time=1) for l in self.ruleoffs]]
                    # *[Write(self.get_horizontal_lines())]]
        return AnimationGroup(*sequence, lag_ratio=0)
    
