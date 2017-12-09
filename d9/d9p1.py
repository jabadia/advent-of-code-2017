from collections import namedtuple

TestCase = namedtuple('TestCase', 'case expected')

TEST_CASES = [
    TestCase("{}", 1),
    TestCase("{{{}}}", 6),
    TestCase("{{},{}}", 5),
    TestCase("{{{},{},{{}}}}", 16),
    TestCase("{<a>,<a>,<a>,<a>}", 1),
    TestCase("{{<ab>},{<ab>},{<ab>},{<ab>}}", 9),
    TestCase("{{<!!>},{<!!>},{<!!>},{<!!>}}", 9),
    TestCase("{{<a!>},{<a!>},{<a!>},{<ab>}}", 3),
]

GARBAGE_PIECES = """
<>
<random characters>
<<<<>
<{!>}>
<!!>
<!!!>>
<{o"i!a,<{i<a>
"""


def check_case(case, actual):
    if actual == case.expected:
        print("%s %d ok" % (case.case, case.expected))
    else:
        print("%s BAD expected %d got %d" % (case.case, case.expected, actual))


def skip_garbage(group):
    assert group[0] == '<'

    while True:
        group = group[1:]
        if group[0] == '>':
            return group[1:]
        elif group[0] == '!':
            group = group[1:]


def parse_group(group, level=1):
    print(group)
    assert group[0] == '{'
    group = group[1:]
    nested_scores = 0
    while True:
        if group[0] == '}':
            return level + nested_scores, group[1:]
        elif group[0] == '<':
            group = skip_garbage(group)
        elif group[0] == '{':
            nested_score, rest = parse_group(group, level + 1)
            nested_scores += nested_score
            group = rest
        else:
            group = group[1:]


for garbage in GARBAGE_PIECES.strip().split('\n'):
    assert skip_garbage(garbage) == ""
    print("skipping %s OK", garbage)

for case in TEST_CASES:
    check_case(case, parse_group(case.case)[0])

with open('input.txt', 'r') as f:
    print(parse_group(f.read()))
