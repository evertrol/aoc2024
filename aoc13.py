import sys


"""

X = n*a + m*c
Y = n*b + m*d

m = (X - n*a) / c
m = (Y - n*b) / d
(X - n*a) * d = (Y - n*b) * c
dX - nad = cY - nbc
dX - cY = nad - nbc = n * (ad - bc)

n = (X - m*c) / a
n = (Y - m*d) / b
(X - m*c) * b  = (Y - m*d) * a
bX - mbc = aY - mad
bx - aY = mbc - mad = m * (bc - ad)

"""

totals = [0, 0]
for line in open(sys.argv[1]):
    line = line.strip()
    if not line:
        continue
    values = [int(string.strip()[2:]) for string in line.split(':')[1].split(',')]
    if line.startswith('Button A'):
        a, b = values
        continue
    elif line.startswith('Button B'):
        c, d = values
        continue
    x, y = values

    for i, offset in enumerate([0, 10000000000000]):
        x, y = x + offset, y + offset

        t, u = d * x - c * y, a * d - b * c
        if t % u:
            # Not possible
            continue
        n = t // u
        t, u = b * x - a * y, b * c - a * d
        if t % u:
            # Not possible
            continue
        m = t // u
        totals[i] += 3 * n + m
print(totals[0], totals[1])
