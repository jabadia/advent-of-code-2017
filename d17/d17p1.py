from collections import namedtuple

TestCase = namedtuple('TestCase', 'case expected')


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase('3', 638),
]


def solve(input):
    jump = int(input)
    buffer = [0]
    next_pos = 0
    for i in range(1, 2018):
        next_pos = (next_pos + jump) % len(buffer)
        buffer = buffer[:next_pos + 1] + [i] + buffer[next_pos + 1:]
        next_pos += 1
        # print(' '.join(['(%d)' % v if i==next_pos else str(v) for i, v in enumerate(buffer)]))
        # pass

    return buffer[(next_pos + 1) % len(buffer)]


INPUT = 356

if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)
    print(solve(INPUT))
