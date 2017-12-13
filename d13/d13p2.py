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
        """, 10),
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
    TestCase((3, 8), 0),
    TestCase((4, 0), 0),
    TestCase((4, 1), 1),
    TestCase((4, 2), 2),
    TestCase((4, 3), 3),
    TestCase((4, 4), 2),
    TestCase((4, 5), 1),
    TestCase((4, 6), 0),
]


def layer_is_at_0_at_t(depth, t):
    return t % (depth + depth - 2) == 0


for c in POS_TEST_CASES:
    depth, t = c.case
    if c.expected == 0:
        assert layer_is_at_0_at_t(depth, t)


def caught_on_trip(firewall, delay):
    max_range = max(firewall.keys())
    for pos in range(0, max_range + 1):
        if pos in firewall:
            if layer_is_at_0_at_t(firewall[pos], pos + delay):  # t = pos + delay
                return True
    return False


def solve(input):
    firewall = {}
    for line in input.strip().split('\n'):
        layer_range, depth = line.strip().split(':')
        firewall[int(layer_range)] = int(depth)
    print(firewall)

    delay = 0
    while caught_on_trip(firewall, delay):
        delay += 1
        if delay % 10000 == 0:
            print(delay)  # progress

    return delay



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
