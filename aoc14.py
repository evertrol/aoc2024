from collections import defaultdict
from math import prod as product
import re
import sys


T = 100
SIZE = [101, 103]

def printgrid(pos):
    m = 0
    for y in range(ysize):
        for x in range(xsize):
            if [x, y] in pos:
                n = pos.count([x, y])
                m += n
                print('*', end='')
            else:
                print('.', end='')
        print()

    
def testtree(pos, minmirrored=100):
    xmid = xsize // 2
    parts = 0
    pairs = [(x, y) for x, y in pos]
    for (x, y) in pairs:
        dx = xmid - x
        x1, x2 = xmid - dx, xmid + dx
        pos1 = (x1, y)
        pos2 = (x2, y)
        if pos1 in pairs and pos2 in pairs:
            parts += 1
    if parts > minmirrored:
        return parts
    return 0

xsize, ysize = SIZE
pos = []
xpos, ypos = [], []
vel = []
xvel, yvel = [], []
for line in open(sys.argv[1]):
    match = re.search(r'p=(\d+),(\d+)\s+v=(-?\d+),(-?\d+)', line)
    xpos.append(int(match.group(1)))
    ypos.append(int(match.group(2)))
    xvel.append(int(match.group(3)))
    yvel.append(int(match.group(4)))
    pos.append([int(match.group(1)), int(match.group(2))])
    vel.append([int(match.group(3)), int(match.group(4))])
backup = [[x, y] for (x, y) in pos]


for t in range(T):
    for i, _ in enumerate(zip(xpos, ypos)):
        xpos[i] += xvel[0]
        ypos[i] += yvel[1]
        xpos[i] %= SIZE[0]
        ypos[i] %= SIZE[1]

grid = defaultdict(int)
quadrants = [0] * 4
xc = SIZE[0] // 2
yc = SIZE[1] // 2
for x, y in zip(xpos, ypos):
    grid[(x, y)] += 1
    if x < xc and y < yc:
        quadrants[0] += 1
    elif x < xc and y > yc:
        quadrants[1] += 1
    elif x > xc and y < yc:
        quadrants[2] += 1
    elif x > xc and y > yc:
        quadrants[3] += 1
score1 = product(quadrants)

xpos = [x for x, _ in backup]
ypos = [y for y, _ in backup]
pos = backup

score2 = 0
for t in range(99999):
    for i in range(len(backup)):
        #xv, yv = xvel[i], yvel[i]
        pos[i][0] += vel[i][0]
        pos[i][1] += vel[i][1]
        pos[i][0] %= SIZE[0]
        pos[i][1] %= SIZE[1]
    if (n := testtree(pos)):
        print()
        printgrid(pos)
        print()
        score2 = t + 1
        break
print(score1, score2)
