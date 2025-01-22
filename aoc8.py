from itertools import combinations
import sys


antennas = {}
for y, line in enumerate(open(sys.argv[1])):
    xmax = len(line) - 2
    for x, char in enumerate(line.strip()):
        if '0' <= char <= '9' or 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            antennas.setdefault(char, []).append((x, y))
ymax = y

positions1, positions2 = set(), set()
for positions in antennas.values():
    for pos1, pos2 in combinations(positions, 2):
        dx, dy = pos2[0] - pos1[0], pos2[1] - pos1[1]

        xl, xh = pos1[0] - dx, pos2[0] + dx
        yl, yh = pos1[1] - dy, pos2[1] + dy
        low, high = (xl, yl), (xh, yh)
        if 0 <= low[0] <= xmax and 0 <= low[1] <= ymax:
            positions1.add(low)
        if 0 <= high[0] <= xmax and 0 <= high[1] <= ymax:
            positions1.add(high)

        x, y = pos1[0], pos1[1]
        while 0 <= x <= xmax and 0 <= y <= ymax:
            positions2.add((x, y))
            x += dx
            y += dy
        x, y = pos1[0] - dx, pos1[1] - dy
        while 0 <= x <= xmax and 0 <= y <= ymax:
            positions2.add((x, y))
            x -= dx
            y -= dy

print(len(positions1), len(positions2))
