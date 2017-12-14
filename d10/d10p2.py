import operator
from functools import reduce
from collections import namedtuple

TestCase = namedtuple('TestCase', 'case expected')

TEST_CASES = [
    TestCase("", "a2582a3a0e66e6e86e3812dcb672a272"),
    TestCase("AoC 2017", "33efeb34ea91902bb2f59c9920caa6cd"),
    TestCase("1,2,3", "3efbe78a8d82f29979031a4aa0b16a9d"),
    TestCase("1,2,4", "63960835bcdc130f0b66d7ff4f6a5a8e"),
]

my_puzzle = "76,1,88,148,166,217,130,0,128,254,16,2,130,71,255,229"


def pad2(s):
    return '0' + s if len(s) == 1 else s


def hex_dense_hash(sparse_hash):
    dense = ""
    while len(sparse_hash):
        block = sparse_hash[:16]
        dense += pad2(hex(reduce(operator.xor, block))[2:])
        sparse_hash = sparse_hash[16:]
    return dense


def knot(l, pos, skip, length):
    l = l[pos:] + l[:pos]
    l = list(reversed(l[:length])) + l[length:]
    npos = -pos % len(l)
    l = l[npos:] + l[:npos]
    pos = (pos + length + skip) % len(l)
    skip += 1
    return l, pos, skip


def solve(input):
    suffix = [int(i) for i in "17, 31, 73, 47, 23".split(',')]
    lengths = [ord(c) for c in input] + suffix
    l = list(range(0, 256))
    pos = 0
    skip = 0
    for i in range(0, 64):
        for length in lengths:
            l, pos, skip = knot(l, pos, skip, length)

    return hex_dense_hash(l)


for c in TEST_CASES:
    actual = solve(c.case)
    assert c.expected == actual

if __name__ == '__main__':
    print(solve(my_puzzle))
