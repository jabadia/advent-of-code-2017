# l = list(range(0, 5))
# lenghts = "3, 4, 1, 5"
l = list(range(0, 256))
lenghts = "76,1,88,148,166,217,130,0,128,254,16,2,130,71,255,229"


def knot(l, pos, skip, length):
    l = l[pos:] + l[:pos]
    l = list(reversed(l[:length])) + l[length:]
    npos = -pos % len(l)
    l = l[npos:] + l[:npos]
    pos = (pos + length + skip) % len(l)
    skip += 1
    return l, pos, skip


lengths = [int(length) for length in lenghts.strip().split(',')]
pos = 0
skip = 0
for length in lengths:
    l, pos, skip = knot(l, pos, skip, length)
    # print(pos)
    # print(' '.join(str(elem) for elem in l))

print(pos)
print(' '.join(str(elem) for elem in l))
print(l[0] * l[1])
