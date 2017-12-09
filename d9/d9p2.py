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

GARBAGE_PIECES = {
    TestCase("<>", 0),
    TestCase("<random characters>", 17),
    TestCase("<<<<>", 3),
    TestCase("<{!>}>", 2),
    TestCase("<!!>", 0),
    TestCase("<!!!>>", 0),
    TestCase('<{o"i!a,<{i<a>', 10),
}


def check_case(case, actual):
    if actual == case.expected:
        print("%s %d ok" % (case.case, case.expected))
    else:
        print("%s BAD expected %d got %d" % (case.case, case.expected, actual))


def count_garbage(group):
    assert group[0] == '<'

    count = 0
    while True:
        group = group[1:]
        count += 1
        if group[0] == '>':
            return group[1:], count - 1
        elif group[0] == '!':
            group = group[1:]
            count -= 1


def parse_group(group, level=1):
    # print(group)
    assert group[0] == '{'
    group = group[1:]
    nested_scores = 0
    garbage_count = 0
    while True:
        if group[0] == '}':
            return level + nested_scores, group[1:], garbage_count
        elif group[0] == '<':
            group, skipped_garbage = count_garbage(group)
            garbage_count += skipped_garbage
        elif group[0] == '{':
            nested_score, rest, skipped_garbage = parse_group(group, level + 1)
            nested_scores += nested_score
            garbage_count += skipped_garbage
            group = rest
        else:
            group = group[1:]


for garbage in GARBAGE_PIECES:
    check_case(garbage, count_garbage(garbage.case)[1])


for case in TEST_CASES:
    check_case(case, parse_group(case.case)[0])

with open('input.txt', 'r') as f:
    print(parse_group(f.read().strip()))
