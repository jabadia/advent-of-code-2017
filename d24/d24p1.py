from collections import namedtuple, defaultdict

TestCase = namedtuple('TestCase', 'case expected')


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase("""
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
""", 31),
]

Bridge = namedtuple('Bridge', 'source target')


def dfs(current, bridges, visited):
    max_val = 0
    for node in bridges[current]:
        if node not in visited:
            max_val = max(
                max_val,
                node.source + node.target + dfs(node.target, bridges,
                                                visited.union([node, Bridge(*reversed(node))]))
            )

    return max_val


def solve(input):
    bridges = defaultdict(list)
    for line in input.strip().split('\n'):
        b = Bridge(*(int(c) for c in line.split('/')))
        r = Bridge(*reversed(b))
        assert b not in bridges[b.source], "%s" % (b,)
        assert r not in bridges[r.source], "%s" % (r,)
        bridges[b.source].append(b)
        bridges[r.source].append(r)

    # for source, b in bridges.items():
    #     print(source, ":", b)

    max_val = dfs(0, bridges, set())
    return max_val


INPUT = """
42/37
28/28
29/25
45/8
35/23
49/20
44/4
15/33
14/19
31/44
39/14
25/17
34/34
38/42
8/42
15/28
0/7
49/12
18/36
45/45
28/7
30/43
23/41
0/35
18/9
3/31
20/31
10/40
0/22
1/23
20/47
38/36
15/8
34/32
30/30
30/44
19/28
46/15
34/50
40/20
27/39
3/14
43/45
50/42
1/33
6/39
46/44
22/35
15/20
43/31
23/23
19/27
47/15
43/43
25/36
26/38
1/10
"""

if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)
    print(solve(INPUT))
