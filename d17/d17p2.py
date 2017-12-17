from collections import namedtuple

TestCase = namedtuple('TestCase', 'case expected')


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase((3, 2018), 1226),
]


def solve(input):
    jump = input[0]
    values = input[1]
    # buffer = [0]
    len_buffer = 1
    next_pos = 0
    found = -1
    for i in range(1, values):
        next_pos = (next_pos + jump) % len_buffer
        # buffer = buffer[:next_pos + 1] + [i] + buffer[next_pos + 1:]
        if next_pos == 0:
            found = i
        len_buffer += 1
        next_pos += 1

    return found


INPUT = 356

if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)
    print(solve((INPUT, 50000000)))
