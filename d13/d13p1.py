from collections import namedtuple

TestCase = namedtuple('TestCase', 'case expected')


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase("""
        0: 3
        1: 2
        4: 4
        6: 4
        """, 24),
]

Layer = namedtuple('Layer', 'range depth')

POS_TEST_CASES = [
    TestCase((2, 0), 0),
    TestCase((2, 1), 1),
    TestCase((2, 2), 0),
    TestCase((3, 0), 0),
    TestCase((3, 1), 1),
    TestCase((3, 2), 2),
    TestCase((3, 3), 1),
    TestCase((3, 4), 0),
    TestCase((3, 5), 1),
    TestCase((3, 6), 2),
    TestCase((3, 7), 1),
]


def layer_pos_at_t(depth, t):
    pos = 0
    dir = +1
    while t:
        pos += dir
        t -= 1
        if pos == depth:
            pos = depth - 2
            dir = -1
        if pos == -1:
            pos = 1
            dir = 1
    return pos


for c in POS_TEST_CASES:
    depth, t = c.case
    check_case(c, layer_pos_at_t(depth, t))


def solve(input):
    firewall = {}
    for line in input.strip().split('\n'):
        lrange, depth = line.strip().split(':')
        firewall[int(lrange)] = int(depth)
    print(firewall)

    max_range = max(firewall.keys())
    pos = 0
    severity = 0

    for pos in range(0, max_range+1):
        if pos in firewall:
            layer_pos = layer_pos_at_t(firewall[pos], pos)  # t = pos
            if layer_pos == 0:
                severity += pos * firewall[pos]

    return severity


INPUT = """
0: 3
1: 2
2: 6
4: 4
6: 4
8: 8
10: 9
12: 8
14: 5
16: 6
18: 8
20: 6
22: 12
24: 6
26: 12
28: 8
30: 8
32: 10
34: 12
36: 12
38: 8
40: 12
42: 12
44: 14
46: 12
48: 14
50: 12
52: 12
54: 12
56: 10
58: 14
60: 14
62: 14
64: 14
66: 17
68: 14
72: 14
76: 14
80: 14
82: 14
88: 18
92: 14
98: 18
"""

if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)
    print(solve(INPUT))
