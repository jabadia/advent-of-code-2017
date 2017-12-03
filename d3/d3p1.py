from collections import namedtuple
import math

TestCase = namedtuple('TestCase', 'case answer')

TEST_CASES = [
    TestCase(1, 0),
    TestCase(2, 1),
    TestCase(3, 2),
    TestCase(4, 1),
    TestCase(5, 2),
    TestCase(6, 1),
    TestCase(7, 2),
    TestCase(8, 1),
    TestCase(9, 2),
    TestCase(10, 3),
    TestCase(11, 2),
    TestCase(12, 3),
    TestCase(21, 4),
    TestCase(22, 3),
    TestCase(23, 2),
    TestCase(24, 3),
    TestCase(25, 4),
]


def dist(n):
    """
    side   last_number   corners         min_dist   max_dist
    1      1             1
    3      9             3 5 7 9         1
    5      25            13 17 21 25     2          4
    """
    if n == 1:
        return 0

    side = math.ceil(math.sqrt(n)) // 2 * 2 + 1
    pos_in_side = (n-((side-2)^2)) % (side - 1)
    radius = side // 2
    offset = abs((side // 2) - pos_in_side)
    dist_to_middle = radius + offset
    print(n, side, pos_in_side, radius, offset)
    return dist_to_middle


def check(case, actual):
    if case.answer != actual:
        print("bad answer for case %d: expected %d, got %d" % (
            case.case, case.answer, actual
        ))
    else:
        print('ok')


for case in TEST_CASES:
    actual = dist(case.case)
    check(case, actual)

print(dist(289326))
