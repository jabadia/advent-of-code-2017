from operator import itemgetter

TEST_STATE = """
0 2 7 0 
"""

INITIAL_STATE = """
14	0	15	12	11	11	3	5	1	6	8	4	9	1	8	4"""


def hash_banks(banks):
    return '|'.join(str(b) for b in banks)


def solve(banks):
    visited = {}
    cycles = 0
    N = len(banks)
    while hash_banks(banks) not in visited:
        visited.update({hash_banks(banks): cycles})
        cycles += 1
        index, blocks = max(enumerate(banks), key=itemgetter(1))
        banks[index] = 0
        while blocks:
            index = (index + 1) % N
            banks[index] += 1
            blocks -= 1
    return cycles - visited[hash_banks(banks)]


res = solve([int(n) for n in INITIAL_STATE.strip().split()])
print(res)
