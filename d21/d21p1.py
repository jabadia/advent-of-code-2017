from collections import namedtuple

TestCase = namedtuple('TestCase', 'iterations case expected')


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


INITIAL = """
.#.
..#
###
"""

TEST_CASES = [
    TestCase(2, """
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
""", 12),
]


def grouped(iterable, n):
    return zip(*[iter(iterable)] * n)


def flatten(list_of_lists):
    return [e for one_list in list_of_lists for e in one_list]


def do_step(board, patterns2, patterns3):
    size = len(board)
    squares = []
    new_board = []
    if size % 2 == 0:
        for rows in grouped(board, 2):
            squares_row = []
            for columns in zip(*[grouped(row, 2) for row in rows]):
                square = '/'.join(''.join(c) for c in columns)
                new_square = patterns2.get(square, None)
                assert new_square is not None, "pattern not found"
                squares_row.append(new_square)
            squares.append(squares_row)
        for squares_row in squares:
            new_board.append(flatten([square[0] for square in squares_row]))
            new_board.append(flatten([square[1] for square in squares_row]))
            new_board.append(flatten([square[2] for square in squares_row]))
    elif size % 3 == 0:
        for rows in grouped(board, 3):
            squares_row = []
            for columns in zip(*[grouped(row, 3) for row in rows]):
                square = '/'.join(''.join(c) for c in columns)
                new_square = patterns3.get(square, None)
                assert new_square is not None, "pattern not found"
                squares_row.append(new_square)
            squares.append(squares_row)
        for squares_row in squares:
            new_board.append(flatten([square[0] for square in squares_row]))
            new_board.append(flatten([square[1] for square in squares_row]))
            new_board.append(flatten([square[2] for square in squares_row]))
            new_board.append(flatten([square[3] for square in squares_row]))
    else:
        assert False, 'bad size'

    return new_board


def rotations_and_flips(pattern):
    flipH = [list(reversed(row)) for row in pattern]
    flipV = list(reversed(pattern))
    rotate90 = list(zip(*pattern[::-1]))
    flipH90 = [list(reversed(row)) for row in rotate90]
    flipV90 = list(reversed(rotate90))
    rotate180 = list(zip(*rotate90[::-1]))
    rotate270 = list(zip(*rotate180[::-1]))
    return [pattern, flipH, flipV, rotate90, rotate180, rotate270, flipV90, flipH90]


def solve(iterations, input):
    patterns2 = {}
    patterns3 = {}
    for line in input.strip().split('\n'):
        p_in, p_out = [p.split('/') for p in line.strip().split(' => ')]
        for p in rotations_and_flips(p_in):
            if len(p) == 2:
                patterns2['/'.join([''.join(row) for row in p])] = p_out
            else:
                patterns3['/'.join([''.join(row) for row in p])] = p_out

    # for p_in, p_out in patterns2.items():
    #     print("%40s => %40s" % (p_in, p_out))
    # for p_in, p_out in patterns3.items():
    #     print("%40s => %40s" % (p_in, p_out))
    board = INITIAL.strip().split('\n')

    for i in range(iterations):
        print(i)
        board = do_step(board, patterns2, patterns3)

    return sum(row.count('#') for row in board)


INPUT = """
../.. => #.#/#../...
#./.. => #.#/#.#/.#.
##/.. => #../.##/##.
.#/#. => ..#/..#/..#
##/#. => ##./.#./#..
##/## => .../.#./.#.
.../.../... => ..#./##.#/#.##/##.#
#../.../... => #.##/..../##../###.
.#./.../... => ##.#/###./#.##/#.#.
##./.../... => ##.#/#.##/.#../##.#
#.#/.../... => ...#/..#./.#.#/.###
###/.../... => ..../#..#/#.##/##..
.#./#../... => .#../.#.#/..#./.###
##./#../... => ..##/#.##/#.../#.#.
..#/#../... => .##./#.##/.#../##..
#.#/#../... => #.../.##./...#/###.
.##/#../... => #.##/..##/.#.#/##..
###/#../... => #..#/...#/..#./...#
.../.#./... => .###/.#../..#./####
#../.#./... => ####/#.../.###/##..
.#./.#./... => ####/#..#/####/#..#
##./.#./... => .#../..##/..##/#..#
#.#/.#./... => .#.#/#.##/#.#./.#.#
###/.#./... => #.##/#.../###./#..#
.#./##./... => ###./#.../..../.###
##./##./... => #.##/###./...#/###.
..#/##./... => .#.#/###./..#./#...
#.#/##./... => #.#./##../##../..##
.##/##./... => ..../..#./.##./.#.#
###/##./... => #.../.#../#.#./#..#
.../#.#/... => ##../#.##/.##./.##.
#../#.#/... => #.#./##.#/.###/.###
.#./#.#/... => ..../####/####/.#.#
##./#.#/... => #.##/.###/##../#...
#.#/#.#/... => ###./..##/#.#./####
###/#.#/... => .##./..../###./....
.../###/... => ###./.##./##../.###
#../###/... => .#../#.../###./...#
.#./###/... => #.#./#.#./####/###.
##./###/... => ...#/##../###./#.#.
#.#/###/... => .#.#/#.#./..#./.##.
###/###/... => ..../#.##/...#/##..
..#/.../#.. => ...#/#.##/#..#/..##
#.#/.../#.. => ..#./##.#/.#.#/..##
.##/.../#.. => ..##/##../#.#./#.##
###/.../#.. => #.##/###./...#/.##.
.##/#../#.. => ##../#.##/##.#/##..
###/#../#.. => #.##/##../.##./.#.#
..#/.#./#.. => #..#/##../.###/#.#.
#.#/.#./#.. => .###/#.##/#.#./####
.##/.#./#.. => #.#./#.../#.##/...#
###/.#./#.. => .##./.#.#/#.#./.#.#
.##/##./#.. => .###/.#.#/...#/#.#.
###/##./#.. => .###/#.##/#.##/#.#.
#../..#/#.. => #.../##../.##./###.
.#./..#/#.. => #.../#.##/#.../###.
##./..#/#.. => ####/..../##.#/.###
#.#/..#/#.. => ..##/##.#/#.##/#..#
.##/..#/#.. => ..#./##.#/#.#./..##
###/..#/#.. => ..##/...#/#..#/#..#
#../#.#/#.. => #.../..../#.../#.##
.#./#.#/#.. => ##../####/.#.#/##..
##./#.#/#.. => .#../..../#.../.##.
..#/#.#/#.. => .#../.#.#/.#.#/..#.
#.#/#.#/#.. => ..#./#.##/#.#./..##
.##/#.#/#.. => #.##/..##/...#/####
###/#.#/#.. => .##./.#.#/###./#..#
#../.##/#.. => ..##/.###/.#../##.#
.#./.##/#.. => #.##/.##./.##./.###
##./.##/#.. => .##./.#../..../..##
#.#/.##/#.. => ..../#.#./##.#/###.
.##/.##/#.. => #..#/..../##.#/..#.
###/.##/#.. => ####/##.#/#..#/##..
#../###/#.. => #.#./###./.###/#...
.#./###/#.. => ##.#/#..#/#.##/..#.
##./###/#.. => ..#./...#/..##/...#
..#/###/#.. => .#.#/..../..##/..##
#.#/###/#.. => #..#/..#./.#../..#.
.##/###/#.. => .#.#/..../#..#/...#
###/###/#.. => #.##/##../.#../....
.#./#.#/.#. => ..../####/.###/.#.#
##./#.#/.#. => #.##/...#/####/####
#.#/#.#/.#. => ..#./##../..../#...
###/#.#/.#. => ####/#.##/###./...#
.#./###/.#. => ...#/..#./...#/..#.
##./###/.#. => .##./#.../.#.#/.###
#.#/###/.#. => ..../..../.#.#/#.##
###/###/.#. => ..#./###./##.#/....
#.#/..#/##. => .###/.#../..#./####
###/..#/##. => #.##/..#./#..#/....
.##/#.#/##. => #.../##../####/.##.
###/#.#/##. => ###./..#./..#./##..
#.#/.##/##. => #.../##../##.#/#.##
###/.##/##. => ..#./#..#/#.##/####
.##/###/##. => .#.#/.###/...#/.#..
###/###/##. => ####/..../.#.#/...#
#.#/.../#.# => ##.#/#..#/.##./...#
###/.../#.# => #.#./.#../...#/...#
###/#../#.# => .#.#/.#../##../##..
#.#/.#./#.# => ###./#.../####/.#.#
###/.#./#.# => ##../#.#./..##/##.#
###/##./#.# => ####/..../###./.##.
#.#/#.#/#.# => ...#/.##./##../.###
###/#.#/#.# => ..#./.##./##.#/.#..
#.#/###/#.# => ...#/..../..#./...#
###/###/#.# => #.#./#.#./##../....
###/#.#/### => #.../##.#/.#../..#.
###/###/### => ##../..#./##../..#.
"""

if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.iterations, case.case)
        check_case(case, result)

    print(solve(5, INPUT))
    print(solve(18, INPUT))
