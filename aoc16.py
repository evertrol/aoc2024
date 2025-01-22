from collections import defaultdict
from math import prod as product
import sys

import numpy as np
from scipy.sparse.csgraph import dijkstra

N, E, S, W = 0, 1, 2, 3  # 'north', 'east', 'south', 'west'
WALKCOST = 1
TURNCOST = 1000

walls = {}
grid = {}
roads = set()
with open(sys.argv[1]) as fp:
    for y, line in enumerate(fp):
        line = line.strip()
        for x, char in enumerate(line):
            if char == '.':
                roads.add((x, y))
            if char == 'S':
                start = (x, y)
                roads.add((x, y))
            if char == 'E':
                end = (x, y)
                roads.add((x, y))
        xmax = len(line)
    ymax = y + 1


def walk(start, heading, path, conns, nodes, deadends):
    pos = start
    headingstart = heading
    cost = 0
    while True:  # pos not in nodes or pos not in deadends:
        # Find the heading that is away from the past
        for nextheading, nextpos in conns[pos]:
            if nextpos not in path:
                path.add(nextpos)
                break
        else:
            break
        if nextpos in nodes or nextpos in deadends:
            path.add(nextpos)
            break
        if nextheading != heading:
            cost += TURNCOST
        cost += WALKCOST
        heading = nextheading
        path.add(pos)
        pos = nextpos
    cost += 2 * WALKCOST
    if nextpos in deadends:
        return (nextpos, cost, (headingstart, heading), path)
    return (nextpos, cost, (headingstart, heading), path)


stack = {'direction': [E]}
pos = start
direction = E
nodes = set()
deadends = set()
conns = defaultdict(set)
for pos in roads:
    n = 0
    for heading, dx, dy in zip((E, S, W, N), (1, 0, -1, 0), (0, 1, 0, -1)):
        test = (pos[0] + dx, pos[1] + dy)
        if test in roads:
            conns[pos].add((heading, test))
            n += 1
    if n > 2:
        nodes.add(pos)
    if n == 1:
        deadends.add(pos)
nodes.add(start)
nodes.add(end)
network = defaultdict(dict)
paths = {}
for i, node in enumerate(nodes):
    for heading, neighbour in conns[node]:
        nextnode, cost, dirs, path = walk(neighbour, heading, {node, neighbour}, conns, nodes, deadends)
        if nextnode:
            network[node].setdefault(nextnode, []).append((cost, dirs[0], dirs[1]))
            paths[((node[0], node[1], heading), (nextnode[0], nextnode[1], dirs[1]))] = path

network2 = defaultdict(dict)
for node, nextnodes in network.items():
    froms = set()
    for nextnode, options in nextnodes.items():
        for (cost, fro, to) in options:
            key1 = (node[0], node[1], fro)
            key2 = (nextnode[0], nextnode[1], to)
            network2[key1][key2] = cost
            froms.add(fro)
    for fro1 in N, E, S, W:
        for fro2 in N, E, S, W:
            if fro1 == fro2:
                continue
            if fro1 == (fro2 + 2) % 4:  # not going back whence we came
                continue
            key1 = (node[0], node[1], fro1)
            key2 = (node[0], node[1], fro2)
            cost = 1000
            network2[key1][key2] = cost

start = start[0], start[1], E
ends = [(end[0], end[1], E), (end[0], end[1], S), (end[0], end[1], W), (end[0], end[1], N)]
if start not in network2:
    for heading in N, S:
        if (start[0], start[1], heading) in network2:
            network2[start][(start[0], start[1], heading)] = TURNCOST
            network2[(start[0], start[1], heading)][start] = TURNCOST

curcost = 0
node = start[0], start[1], E
costs = {node: curcost}
heading = E
done = set()
finalcost = 9e9
curtiles = {(node[0], node[1])}
ntiles = {node: curtiles}
while True:
    x, y, heading = node
    conns = network2[node]
    for nextnode, cost in conns.items():
        if nextnode in done:
            continue
        path = paths.get((node, nextnode), set())
        tiles = curtiles | path
        cost += curcost
        if cost > finalcost:
            continue
        if nextnode in costs:
            if cost < costs[nextnode]:
                costs[nextnode] = cost
                ntiles[nextnode] = tiles
            elif cost == costs[nextnode]:
                ntiles[nextnode] |= tiles
        else:
            costs[nextnode] = cost
            ntiles[nextnode] = tiles
    costs.pop(node)
    done.add(node)
    if len(costs) == 0:
        break
    data = sorted((value, key) for key, value in costs.items())
    curcost, node = data[0]
    curtiles = ntiles[node]
    if (node[0], node[1]) == end:
        finalnode = node
        if finalcost > 8e9:
            finalcost = curcost
        break

print(finalcost, len(ntiles[finalnode]))
