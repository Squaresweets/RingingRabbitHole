import re
from copy import deepcopy
from BellEnd.Helper import *

class Method:
    def __init__(self, stage, notation, calls, ruleoffsStart, ruleoffsEvery):
        self.stage = stage
        self.notation = notation
        self.calls = calls
        self.ruleoffsStart = ruleoffsStart
        self.ruleoffsEvery = ruleoffsEvery

class Calls:
    def __init__(self, bob_notation, single_notation, start, every, cover):
        self.bob_notation = split_notation(bob_notation)
        self.single_notation = split_notation(single_notation)
        self.start = start
        self.every = every
        self.cover = cover

class MethodLine:
    def __init__(self, positions, indexes, notation, stage):
        self.positions = positions
        self.indexes = indexes
        self.notation = notation
        self.stage = stage
        self.ruleoffs = []
        self.labels = {}
        self.huntBells = []
        self.placeBellPositions = []

    @property
    def Len(self):
        return len(self.positions)

class CompositionPart:
    def __init__(self, touchType, callingPos="", id_str=''):
        self.touch_type = 'b' if touchType in ('', '-') else touchType
        self.calling_pos = callingPos
        self.splice_id = -1 if id_str == '' else int(id_str)

class Composition:
    def __init__(self, observationBell, notation, num_rounds=-1, dont_stop_till_end_of_comp=False):
        self.plain = len(notation) == 0
        self.observationBell = observationBell
        self.num_rounds = num_rounds
        self.dont_stop_till_end_of_comp = dont_stop_till_end_of_comp
        self.comp_notation = notation
    def plain():
        return Composition(-1, [])

class LineGenerator:
    line = None
    bells = []
    indexBells = [-1]
    initialBells = []
    m = None

    @staticmethod
    def generate_line(methods, composition = Composition.plain(), lead_end_cap=-1, initial_row=None):
        lg = LineGenerator
        lg.m = methods[0]

        # determine starting stage
        initial_stage = max(m.stage for m in methods)

        notation_parts = split_notation(expand_notation(lg.m.notation))
        lg.line = MethodLine([], [], notation_parts, initial_stage)
        if not composition.plain:
            lg.line.notation = []


        lg.initialBells = list(range(1, initial_stage + 1)) if initial_row == None else initial_row.copy()
        lg.bells = lg.initialBells[:]
        lg.indexBells = [0] + lg.bells[:]
        lg.insert_bells_into_line()

        lg.line.huntBells = lg.initialBells[:]

        lead_end_counter = 0
        round_counter = 0
        touch_counter = -lg.m.calls.start
        rule_off_from = lg.m.ruleoffsStart
        old_line_len = 0
        comp_call_counter = 0
        lead_ends_since_last_touch = []

        for _ in range(1024):
            i = 0
            while i < len(notation_parts):
                n = notation_parts[i]

                should_call = (not composition.plain
                                and (touch_counter + 1) % lg.m.calls.every == 0
                                and comp_call_counter < len(composition.comp_notation))
                if should_call:
                    c = composition.comp_notation[comp_call_counter]
                    cover = lg.m.calls.cover
                    touch_not = [''] * cover
                    if c.touch_type == 'b' and lg.m.calls.bob_notation:
                        touch_not = lg.m.calls.bob_notation
                    elif c.touch_type == 's' and lg.m.calls.single_notation:
                        touch_not = lg.m.calls.single_notation
                    else:
                        touch_not = notation_parts[i:i + cover]
                        c.touch_type = 'p'

                    lg.apply_notation_multi(touch_not)

                    if c.calling_pos:
                        obs = composition.observation_bell if composition.observation_bell != -1 else lg.m.stage
                        new_pos = lg.bells.index(obs) + 1
                        calling_pos = calculate_calling_positions(new_pos, lg.m.stage, touch_not[-1])
                        if c.calling_pos not in calling_pos:
                            lg.revert(len(touch_not))
                            lg.apply_notation(n)
                            i += 1
                            continue

                    comp_call_counter += 1
                    i += len(touch_not)
                    touch_counter += len(touch_not)
                    lead_ends_since_last_touch.clear()
                    if c.touch_type != 'p':
                        lg.line.labels[lg.line.Len - len(touch_not) - 1] = f"-{c.touch_type}"

                    if c.splice_id != -1:
                        lg.m = methods[c.splice_id]
                        touch_counter = -lg.m.calls.start
                        rule_off_from = lg.line.Len - 1 + lg.m.ruleoffsStart
                        notation_parts = split_notation(expand_notation(lg.m.notation))
                        lg.line.labels[lg.line.Len] = abbreviate_title(lg.m.title, lg.m.stage)
                        break
                    continue

                lg.apply_notation(n)
                touch_counter += 1
                i += 1

                if lg.m.ruleoffsEvery:
                    while old_line_len < lg.line.Len:
                        if (old_line_len - rule_off_from) % lg.m.ruleoffsEvery == 0:
                            lg.line.ruleoffs.append(old_line_len - 1)
                        old_line_len += 1

            for idx, val in enumerate(lg.bells):
                if val != lg.initialBells[idx] and val in lg.line.huntBells:
                    lg.line.huntBells.remove(val)

            lg.line.placeBellPositions.append(lg.line.Len - 1)

            lead_end_counter += 1
            if lead_end_cap != -1 and lead_end_counter >= lead_end_cap:
                return lg.line

            if lg.bells == lg.initialBells:
                if not (composition.dont_stop_till_end_of_comp and comp_call_counter < len(composition.comp_notation)):
                    round_counter += 1
                    if composition.num_rounds == -1 or round_counter >= composition.num_rounds:
                        break
                lead_ends_since_last_touch.clear()

            bells_str = ''.join(map(str, lg.bells))
            if bells_str in lead_ends_since_last_touch:
                break
            lead_ends_since_last_touch.append(bells_str)

        return lg.line

    @staticmethod
    def insert_bells_into_line():
        lg = LineGenerator
        lg.line.positions.append(lg.bells[:])
        lg.indexBells = [0] + [0] * lg.line.stage
        for i in range(lg.line.stage):
            lg.indexBells[lg.bells[i]] = i
        lg.line.indexes.append(lg.indexBells[:])

    @staticmethod
    def apply_notation_multi(lst):
        for n in lst:
            LineGenerator.apply_notation(n)

    @staticmethod
    def revert(num):
        lg = LineGenerator
        lg.line.indexes = lg.line.indexes[:-num]
        lg.indexBells = lg.line.indexes[-1][:]
        lg.line.positions = lg.line.positions[:-num]
        lg.bells = lg.line.positions[-1][:]

    @staticmethod
    def apply_notation(n):
        lg = LineGenerator
        m = lg.m
        if n == 'x':
            for i in range(0, m.stage - 1, 2):
                lg.bells[i], lg.bells[i + 1] = lg.bells[i + 1], lg.bells[i]
        else:
            if '(' in n:
                def repl(match):
                    a, b = match.group(1)
                    first = bell_string_to_value[a]
                    second = bell_string_to_value[b]
                    tmp = lg.bells[first - 1]
                    lg.bells.pop(first - 1)
                    lg.bells.insert(second - 1, tmp)
                    return ''.join(bell_value_to_string[i]
                                   for i in range(min(first, second), max(first, second) + 1))
                n = re.sub(r"\((..)\)", repl, n)

            elif '[' in n:
                for match in re.finditer(r"\[(.*?)\]", n):
                    j = match.group(1)
                    start = min(bell_string_to_value[c] for c in j) - 1
                    vals = lg.bells[start:start + len(j)]
                    for idx, c in enumerate(j):
                        lg.bells[start + idx] = vals[bell_string_to_value[c] - start - 1]

            i = 1
            while i < m.stage:
                cur = bell_value_to_string[i]
                nxt = bell_value_to_string[i + 1]
                if nxt in n:
                    i += 1
                elif cur not in n:
                    lg.bells[i - 1], lg.bells[i] = lg.bells[i], lg.bells[i - 1]
                    i += 1
                i += 1

        LineGenerator.insert_bells_into_line()

    @staticmethod
    def add_cover_bell(line):
        n = line.stage + 1
        for pos, idx in zip(line.positions, line.indexes):
            pos.append(n)
            idx.append(n - 1)
        line.stage += 1
        line.huntBells.append(n)

    @staticmethod
    def add_extra_rounds(line):
        for _ in range(2):
            line.positions.insert(0, deepcopy(line.positions[0]))
            line.indexes.insert(0, deepcopy(line.indexes[0]))
        line.labels = {k + 2: v for k, v in line.labels.items()}
        line.ruleoffs = [i + 2 for i in line.ruleoffs]