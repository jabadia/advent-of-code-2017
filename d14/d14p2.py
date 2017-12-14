from collections import namedtuple

from d10.d10p2 import solve as calculate_hash

TEST_INPUT = 'flqrgnkx'
INPUT = 'wenycdww'

TestCase = namedtuple('TestCase', 'case expected')


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase('flqrgnkx', 1242),
]


def pad128(s):
    return '0' * (128 - len(s)) + s


def calculate_grid(input):
    grid = []
    for row_key in ['%s-%d' % (input, row) for row in range(0, 128)]:
        hash = calculate_hash(row_key)
        row = [c for c in pad128(bin(int(hash, 16))[2:])]
        assert len(row) == 128
        grid.append(row)
    return grid


def neighbours(i, j):
    if i > 0:
        yield (i - 1, j)
    if j > 0:
        yield (i, j - 1)
    if i < 127:
        yield (i + 1, j)
    if j < 127:
        yield (i, j + 1)


def dfs(grid, i0, j0):
    for i, j in neighbours(i0, j0):
        if grid[i][j] == '1':
            grid[i][j] = 'v'
            dfs(grid, i, j)


def solve(input):
    grid = calculate_grid(input)

    print('finding components')
    components = 0
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            if v == '1':
                dfs(grid, i, j)
                components += 1
    return components


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)

    print(INPUT, solve(INPUT))
