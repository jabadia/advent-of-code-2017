from collections import namedtuple

TestCase = namedtuple('TestCase', 'case expected')


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase('65,8921', 588),
]


def pad32(s):
    return '0' * (32 - len(s)) + s


def solve(input):
    val_a, val_b = [int(n) for n in input.split(',')]
    divisor = 2147483647
    factor_a = 16807
    factor_b = 48271

    matches = 0
    for i in range(0, 40000000):
        val_a = (val_a * factor_a) % divisor
        val_b = (val_b * factor_b) % divisor
        if val_a & 0xffff == val_b & 0xffff:
            matches += 1
            # print('match')
            # if matches == 588:
            #     print(i)
        # else:
        # print('-')

        if i % 100000 == 0 and i != 0:
            print(i)
    return matches


input = '512,191'

if __name__ == '__main__':
    # for case in TEST_CASES:
    #     result = solve(case.case)
    #     check_case(case, result)
    print(solve(input))
