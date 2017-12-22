from collections import namedtuple, defaultdict

TestCase = namedtuple('TestCase', 'case iterations expected')


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase("""
..#
#..
...
    """, 70, 41),
    TestCase("""
..#
#..
...
""", 10000, 5587),
]

N = 0  # clockwise
E = 1
S = 2
W = 3

# sides
RIGHT = +1
LEFT = -1


def turn(direction, side):
    return (direction + side) % 4


assert turn(N, RIGHT) == E
assert turn(N, LEFT) == W
assert turn(S, RIGHT) == W
assert turn(S, LEFT) == E

Vector = namedtuple('Vector', "x y")

directions = {
    N: Vector(0, -1),  # equiv. Vector(x=0, y=-1)
    E: Vector(1, 0),
    S: Vector(0, 1),
    W: Vector(-1, 0),
}


def advance(pos, direction):
    delta = directions[direction]
    return Vector(pos.x + delta.x, pos.y + delta.y)
    # return Vector(*map(sum, zip(pos, delta)))


def print_board(board, pos):
    min_r, max_r = min(pos.y, *[v[1] for v in board.keys()]), max(pos.y, *[v[1] for v in board.keys()])
    min_c, max_c = min(pos.x, *[v[0] for v in board.keys()]), max(pos.x, *[v[0] for v in board.keys()])
    for r in range(min_r, max_r+1):
        print(''.join(('[%s]' if pos == Vector(c, r) else ' %s ') % board[(c, r)] for c in range(min_c, max_c+1)))


def solve(input, iterations):
    board = defaultdict(lambda:'.')
    rows = input.strip().split('\n')
    size = len(rows)
    for r, row in enumerate(rows):
        print(row)
        for c, cell in enumerate(row):
            board[(c, r)] = cell

    pos = Vector(size // 2, size // 2)
    dir = N
    bursts = 0
    for i in range(iterations):
        # print(i, pos, dir)
        # print_board(board, pos)
        current = board[(pos.x, pos.y)]
        if current == '#':
            dir = turn(dir, RIGHT)
            board[(pos.x, pos.y)] = '.'
        else:
            dir = turn(dir, LEFT)
            board[(pos.x, pos.y)] = '#'
            bursts += 1

        pos = advance(pos, dir)
        pass

    return bursts  #list(board.values()).count('#')

INPUT = """
.##..#.#.##...#....#..###
####.#...###.####..#.....
#.#.#####....######.###.#
#.#..###.#.#####....#..#.
####.#.#...#.##.##..#.###
#.####..#####.#.#....#.##
.#.####.#....###..##....#
..##.#..##.#.#.###.##.#..
##....#....######.###.###
.#.##.###.###.###.#..#.#.
#.##.#.#..#.#.....###....
####.....#..###..##..##..
##....#.#...####...#.#.#.
...#.##..###..##..#......
#....#..##.##.#..#.###..#
...#...##.##.##...#.#.#..
.##....#.####.#..##.#...#
#.######......#.#...#.##.
#.##....###...###.###....
#..#.#.#.#.#..#.#.....#..
...##..##.###....#.###...
.######.#...###.###.#.#.#
####..###.####...#..#####
.##.#.##...##..##...#.#.#
###...##..#..##.##..#..#.
"""

if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case, case.iterations)
        check_case(case, result)

    print(solve(INPUT, 10000))
