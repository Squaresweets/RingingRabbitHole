import re

bell_string_to_value = {
    "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "0":10, "E":11, "T":12,
    "A":13, "B":14, "C":15, "D":16, "F":17, "G":18, "H":19, "J":20, "K":21, "L":22
}
bell_value_to_string = ['?', '1','2','3','4','5','6','7','8','9','0','E','T','A','B','C','D','F','G','H','J','K','L']

def split_notation(n):
    return [x for x in re.split(r'\.|(x)', n) if x and x != '.']

def reverse_notation(s):
    if '(' in s:
        parts = re.split(r'[()]', s)
        if len(parts[1]) >= 2:
            return parts[0] + "(" + parts[1][1] + parts[1][0] + ")" + parts[2]
    elif '[' in s:
        parts = re.split(r'([\[\]])', s)
        for i in range(len(parts)):
            if parts[i] == '[':
                current = parts[i + 1]
                min_index = min(bell_string_to_value[c] for c in current)
                inverted = [''] * len(current)
                for j, ch in enumerate(current):
                    idx = bell_string_to_value[ch] - min_index
                    inverted[idx] = bell_value_to_string[j + min_index]
                parts[i + 1] = ''.join(inverted)
        return ''.join(parts)
    return s

def expand_notation(n):
    if ',' not in n:
        return n
    strings = n.split(',')
    jump = '(' in n or '[' in n
    for c in range(len(strings)):
        x = split_notation(strings[c])
        if len(x) == 1:
            continue
        if jump:
            x = [reverse_notation(part) for part in x]
        strings[c] += '.' + '.'.join(list(reversed(x))[1:])
    return '.'.join(strings).replace('.x.', 'x')

def calculate_calling_positions(p: int, stage: int, n: str) -> str:
    result = ""
    if p == stage:
        result += 'h'
    elif p == stage - 1:
        result += 'w' if stage % 2 == 0 else 'm'
    elif p == stage - 2:
        result += 'm' if stage % 2 == 0 else 'w'

    if '2' in n or ('1' in n and '3' in n):
        if p == 2:
            result += 'b'
    elif p == 3:
        result += 'b'

    if p == 3:
        result += 't'

    extra = "??iofvxsenacdgjklpqru"
    if p < len(extra):
        result += extra[p]

    return result

def abbreviate_title(title: str, stage: int) -> str:
    parts = title.split(" ")
    abbr = ""
    for i, part in enumerate(parts[:-1]):
        if i == 0:
            abbr += part[:3]
        else:
            abbr += part[0].upper()
    if len(abbr) > 6:
        abbr = abbr[:6]
    return abbr + bell_value_to_string[stage]