import sys


grid = {}
for y, line in enumerate(open(sys.argv[1])):
    for x, char in enumerate(line.strip()):
        grid[(x, y)] = int(char)
    xmax = x + 1
ymax = y + 1

# Set negative border
for x in range(-1, xmax+1):
    grid[(x, -1)] = -99
    grid[(x, ymax)] = -99
for y in range(-1, ymax+1):
    grid[(-1, y)] = -99
    grid[(xmax, y)] = -99

# Obtain a nested dictionary:
# height-difference -> height value -> position -> list of neighbours
# The list of neighbours is a list of positions that have this specific
# height difference with `position` and `value`.
steps = {}
for pos, value in grid.items():
    if value < 0:
        continue
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        neighbour = (pos[0]+dx, pos[1]+dy)
        step = grid[neighbour] - grid[pos]
        steps.setdefault(step, {}).setdefault(value, {}).setdefault(pos, []).append(neighbour)

total = 0
variants = set()
# Work top-down: start at 9, count when 0 is reached
for pos, paths in steps[-1][9].items():
    start = pos
    i = {height: 0 for height in range(10)}
    height = 9
    positions = {height: pos}
    while height < 10:
        pos = positions[height]
        if pos not in steps[-1][height]:
            i[height] = 0
            height += 1
            continue
        paths = list(steps[-1][height][pos])
        if i[height] >= len(paths):
            i[height] = 0
            height += 1
            if height > 9:
                break
            continue
        pos = paths[i[height]]
        i[height] += 1
        height -= 1
        positions[height] = pos
        if height == 0:
            total += 1
            variants.add((start, pos))
            height += 1
            continue
        if height > 8:
            break
print(len(variants), total)


# More generic variant
# Pick up or down; pick a (single) stepsize
upwards = True
delta, startheight, endheight = (1, 0, 9) if upwards else (-1, 9, 0)

npaths = 0
variants = set()
selsteps = steps[delta]
for pos, paths in selsteps[startheight].items():
    start = pos
    i = {height: 0 for height in range(max(startheight, endheight)+1)}
    height = startheight
    positions = {height: pos}
    while height != startheight-delta:
        pos = positions[height]
        if pos not in selsteps[height]:
            i[height] = 0
            height -= delta
            continue
        paths = list(selsteps[height][pos])
        if i[height] >= len(paths):
            i[height] = 0
            height -= delta
            if height == startheight  - delta:
                break
            continue
        pos = paths[i[height]]
        i[height] += 1
        height += delta
        positions[height] = pos
        if height == endheight:
            npaths += 1
            variants.add((start, pos))
            height -= delta
            continue
        if height == startheight:
            break
print(len(variants), npaths)
