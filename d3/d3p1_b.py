from collections import namedtuple

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
    TestCase(1024, 31),
]


def check(case, actual):
    if case.answer != actual:
        print("bad answer for case %d: expected %d, got %d" % (
            case.case, case.answer, actual
        ))
    else:
        print('ok')


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
    N: Vector(0, 1),  # equiv. Vector(x=0, y=1)
    E: Vector(1, 0),
    S: Vector(0, -1),
    W: Vector(-1, 0),
}


def advance(pos, direction):
    delta = directions[direction]
    return Vector(pos.x + delta.x, pos.y + delta.y)
    # return Vector(*map(sum, zip(pos, delta)))


def solve(N):
    board = {}
    pos, dir = Vector(0, 0), E
    n = 1
    board[pos] = n
    while n < N:
        n += 1
        pos = advance(pos, dir)
        board[pos] = n
        if not board.get(advance(pos, turn(dir, LEFT)), None):
            dir = turn(dir, LEFT)

    return abs(pos[0]) + abs(pos[1])


for case in TEST_CASES:
    actual = solve(case.case)
    check(case, actual)

print(solve(289326))
