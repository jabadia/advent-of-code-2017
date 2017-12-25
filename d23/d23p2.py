a = 1
b = 81
c = b
d = 0
e = 0
f = 0
g = 0
h = 0

if a != 0:
    b = b * 100
    b = b + 100000
    c = b
    c += 17000

while b <= c:
    f = 1
    d = 2
    half_b = b // 2
    while d <= half_b and f == 1:
        e = 2
        # while e < half_b and f == 1:
        #     if e * d == b:
        #         f = 0
        #         break
        #     e += 1
        if b % d == 0:
            f = 0
            break
        d += 1

    if f == 0:
        h += 1

    print(a, b, c, d, e, f, g, h)
    # if b == c:
    #     break
    #
    b += 17

print(h)
