import sys

lines = open(sys.argv[1]).read().strip().split('\n')
xmax = len(lines[0])
ymax = len(lines)
lines = ['.' * xmax] + lines + ['.' * xmax]
lines = ['.' + line + '.' for line in lines]


def walk(start, char, network, grid):
    x, y = start
    network.add((x, y))
    for dx, dy in zip((1, 0, -1, 0), (0, 1, 0, -1)):
        if (x+dx, y+dy) not in network and char == grid[y+dy][x+dx]:
            walk((x+dx, y+dy), char, network, grid)


overlap = {}
nplots = {}
networks = {}
inet = 1
tested = set()
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == '.':
            continue
        if (x, y) in tested:
            continue
        network = set()
        walk((x, y), char, network, lines)
        networks[(x, y)] = network
        tested |= network
        continue

total = 0
overlap = {}
for key, network in networks.items():
    area = len(network)
    overlap = 0
    for pos in network:
        for dx, dy in zip((1, 0, -1, 0), (0, 1, 0, -1)):
            if (pos[0]+dx, pos[1]+dy) in network:
                overlap += 1
    price = area * (4 * area - overlap)
    total += price
total1 = total


def find_edge(pos, edge, network, side):
    if pos not in network:
        return
    if pos in edge:
        return
    x, y = pos
    if side == 'n':
        neighbour = x, y-1
        if neighbour in network:
            return
        edge.append(pos)
        find_edge((x-1, y), edge, network, side)
        find_edge((x+1, y), edge, network, side)
    if side == 's':
        neighbour = x, y+1
        if neighbour in network:
            return
        edge.append(pos)
        find_edge((x-1, y), edge, network, side)
        find_edge((x+1, y), edge, network, side)
    if side == 'w':
        neighbour = x-1, y
        if neighbour in network:
            return
        edge.append(pos)
        find_edge((x, y-1), edge, network, side)
        find_edge((x, y+1), edge, network, side)
    if side == 'e':
        neighbour = x+1, y
        if neighbour in network:
            return
        edge.append(pos)
        find_edge((x, y-1), edge, network, side)
        find_edge((x, y+1), edge, network, side)


price = 0
for key, network in networks.items():
    area = len(network)
    xs = [x for x, _ in network]
    ys = [y for _, y in network]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    alledges = {'n': [], 's': [], 'e': [], 'w': []}
    edges = {}
    for pos in network:
        edges[pos] = {'n': [], 's': [], 'e': [], 'w': []}
        for side in 'nsew':
            if pos in alledges[side]:
                continue
            edge = []
            find_edge(pos, edge, network, side)
            alledges[side].extend(edge)
            edges[pos][side] = edge
    total = 0
    nsides = 0
    for edge in edges.values():
        nsides += sum(1 for side in edge.values() if side)
        for side in edge.values():
            total += len(side)
    price += area * nsides
print(total1, price)
