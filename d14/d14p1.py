from collections import namedtuple

from d10.d10p2 import solve as calculate_hash

TEST_INPUT = 'flqrgnkx'
INPUT = 'wenycdww'

GRID = """
##.#.#..
.#.#.#.#   
....#.#.   
#.#.##.#   
.##.#...   
##..#..#   
.#...#..   
##.#.##.
"""

TestCase = namedtuple('TestCase', 'case expected')


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase('flqrgnkx', 8108),
]

def pad2(s):
    return '0' + s if len(s) == 1 else s

def solve(input):
    used = 0
    for row_key in ['%s-%d' % (input, row) for row in range(0, 128)]:
        hash = calculate_hash(row_key)
        used += bin(int(hash,16)).count('1')
    return used


if __name__ == '__main__':

    for row in GRID.strip().split('\n'):
        row = row.strip().replace('#','1').replace('.','0')
        print(row, pad2(hex(int(row,2))[2:]))

    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)

    print(INPUT, solve(INPUT))
