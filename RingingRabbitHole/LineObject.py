from manim import *
from BellEnd.LineGenerator import *
from BellEnd.Helper import *
from BellTexts import * 

BELL_COLORS = ['#4073EE', '#48DD00', '#D511E0', '#DCDD00', '#4DDDDE', '#386754', '#AA7700', '#EE5B56', '#756BFF', '#185BE1', '#009018', '#F100FF', '#FEFF00', '#00FFB1', '#083321', '#FFB200', '#FF0800', '#8E86FF', '#3500FF', '#FFFFFF']
HUNT_BELL_COLOR = "#FF3636"
GRID_SPACING = 0.15

class LineObject(Mobject):
    def __init__(self, line):
        self.stage = line.stage
        super().__init__()

        self.table_data = [b for row in line.positions for b in row]

        #Create all the dummy objects that we use as anchors and stuff
        self.anchors = Group()
        # self.anchors.add(*[Point().set_z_index(-1000) for _ in self.table_data]) #Create dummy objects for all the positions
        self.anchors.add(*[Circle().scale(0.05).set_z_index(-1000) for _ in self.table_data]) #Create dummy objects for all the positions
        self.anchors.arrange_in_grid(cols=self.stage, buff=GRID_SPACING)
        self.add(self.anchors)

        leLen = len(line.notation) * line.stage
        self.leads = Group(
            Group(*self.anchors[:leLen+line.stage]),
            *[
                Group(*self.anchors[i:i + leLen])
                for i in range(leLen+line.stage, len(self.anchors), leLen)
            ]
        )

        #Bell texts
        #Put the actual text in, tied to the position of the dummies
        self.bell_texts = [VGroup() for _ in range(self.stage)] #Vgroup of vgroups of bells, each bell has its own vgroup, 0 indexed
        self.all_bell_texts = VGroup()
        for i in range(len(self.table_data)):
            bell_num = self.table_data[i]
            t = BellText(bell_num, self.anchors[i])
            self.add(t)
            self.bell_texts[bell_num-1].add(t)
            self.all_bell_texts.add(t)

            #check if second in lead
            if (i//self.stage)%len(line.notation) == 1 and (i//self.stage) != 1:
                t.add_secondary_bell(self.bell_texts[bell_num-1][-2].get_anchor_position())

        #Add in the ruleoffs
        self.ruleoffs = VGroup()
        self.add(self.ruleoffs)
        def make_ruleoff_updater(h):
            def ruleoff_updater(mob):
                # Makes sense to have this use get anchor as it doesn't depend on the position?
                # I'm going to assume the positions of the ruleoffs will never need to change
                positions = [(self.get_anchor_from_pos((h,0)).get_center() +
                              self.get_anchor_from_pos((h+1,0)).get_center())/2,
                             (self.get_anchor_from_pos((h,self.stage-1)).get_center() +
                              self.get_anchor_from_pos((h+1,self.stage-1)).get_center())/2]
                mob.set_points_as_corners(positions)
            return ruleoff_updater
        for h in line.ruleoffs:
            if h > len(line.positions) or h < 0:
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
                positions = [g.get_anchor_position() for g in self.get_bell_text_entries(b_val)]

                mob.clear_points()
                # Make it so if we go up we make it split the path
                mob.start_new_path(positions[0])
                for i in range(1, len(positions)):
                    if positions[i][1] > positions[i - 1][1]:
                        mob.start_new_path(positions[i])
                    else:
                        mob.add_line_to(positions[i])
            return line_updater

        for b in range(line.stage):
            l = self.bell_lines[b]

            l.add_updater(make_line_updater(b+1))
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

    def get_bell_text_entry(self, bell, row): #row is 0 indexed
        return self.bell_texts[bell-1][row]
    
    def get_bell_text_entries(self, bell):
        positions = []
        for bt in self.bell_texts[bell-1]:
            positions.extend(bt.get_primary_and_secondary())
        return positions

    def get_anchor_from_pos(self, pos): 
        return self.anchors[pos[1]+pos[0]*self.stage]

    def set_bell_visible(self, bell, visible):
        bellEntries = self.get_bell_text_entries(bell)
        for e in bellEntries:
            e.primary_text.set_opacity(visible)
    
    def set_line_visible(self, bell, visible, also_change_numbers=True):
        self.bell_lines[bell-1].set_opacity(visible)
        self.bell_lines[bell-1].set_fill(opacity=0)
        if also_change_numbers:
            self.set_bell_visible(bell, not visible)
    
    def animate_line_visible(self, bell, visible):
        if visible:
            self.set_line_visible(bell, True, False)
            sequence = [Create(self.bell_lines[bell-1], rate_func=smoothstep, run_time=1),
                    AnimationGroup(*[Unwrite(l.primary_text) for l in self.get_bell_text_entries(bell)], lag_ratio=0.1, run_time=1)]
        else:
            self.set_bell_visible(bell, True)
            sequence = [Uncreate(self.bell_lines[bell-1],rate_func=smoothstep, run_time=1),
                    AnimationGroup(*[Write(l.primary_text) for l in reversed(self.get_bell_text_entries(bell))], lag_ratio=0.1, run_time=1)]

        return Succession(AnimationGroup(*sequence, lag_ratio=0),
                            UpdateFromFunc(None, lambda m: self.set_line_visible(bell, visible), run_time=0))
    
    def reveal(self):
        sequence = [Write(self.all_bell_texts, rate_func=smoothstep, run_time=1),
                    *[Create(l, rate_func=smoothstep, run_time=1) for l in self.bell_lines],
                    *[Create(l, rate_func=smoothstep, run_time=1) for l in self.ruleoffs]]
                    # *[Write(self.get_horizontal_lines())]]
        return AnimationGroup(*sequence, lag_ratio=0)

    def unreveal(self):
        sequence = [Unwrite(self.all_bell_texts, rate_func=smoothstep, run_time=1),
                    *[Uncreate(l, rate_func=smoothstep, run_time=1) for l in self.bell_lines],
                    *[Uncreate(l, rate_func=smoothstep, run_time=1) for l in self.ruleoffs]]
                    # *[Write(self.get_horizontal_lines())]]
        return AnimationGroup(*sequence, lag_ratio=0)
    
    def horizontal_leads(self):
        for bt in self.all_bell_texts:
            bt.show_extra_lead_head()
        return self.leads.animate.arrange(direction=RIGHT, buff=0.5)
    
