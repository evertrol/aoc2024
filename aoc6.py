import time
from typing import NamedTuple
from itertools import cycle


class Position(NamedTuple):
    x: int
    y: int

class Guard(NamedTuple):
    pos: Position
    heading: str

moves = {
    'U': Position(0, -1),
    'R': Position(1, 0),
    'D': Position(0, 1),
    'L': Position(-1, 0),
}
headings = cycle(moves.keys())


def read(fname):
    grid = {}
    xmax = ymax = 0
    with open(fname) as fp:
        for y, line in enumerate(fp):
            line = line.strip()
            xmax = len(line)
            ymax += 1
            for x, char in enumerate(line):
                grid[(x, y)] = '.'
                if char == '#':
                    grid[(x, y)] = '#'
                elif char == '^':
                    guard = Guard(Position(x, y), 'U')
    return grid, guard, (xmax, ymax)


def walk(grid, guard, existing=None):
    if not existing:
        existing = []
    place0 = guard.pos
    places = {place0}
    while next(headings) != guard.heading:
        pass
    guards = {guard}
    loop = False
    while True:
        move = moves[guard.heading]
        newpos = Position(guard.pos.x + move.x, guard.pos.y + move.y)
        if newpos in grid:
            if grid[newpos] == '#':
                guard = Guard(guard.pos, next(headings))
                if guard in guards:
                    loop = True
                    break
                guards.add(guard)
            else:
                guard = Guard(newpos, guard.heading)
                if guard in guards:
                    loop = True
                    break
                places.add(newpos)
                guards.add(guard)
        else:
            break
    return places, guards, loop

def run(grid, guard):
    guard0 = guard
    t = time.perf_counter()
    places, guards, _ = walk(grid, guard)
    dt = time.perf_counter() - t
    guard = guard0
    total1 = len(places)

    starting_grid = grid.copy()
    loops = 0
    prevguard = guard0
    places = {guard0.pos}
    for i, guard in enumerate(guards):
        grid = starting_grid.copy()
        place = guard.pos
        if place in places:
            prevguard = guard
            continue
        places.add(place)
        grid[place] = '#'
        t = time.perf_counter()
        _, _, loop = walk(grid, guard0)
        dt = time.perf_counter() - t
        prevguard = guard
        loops += loop
    total2 = loops

    return total1, total2


def main(fname):
    grid, guard, size = read(fname)
    total1, total2 = run(grid, guard)
    print(total1, total2)


if __name__ == '__main__':
    import sys
    main(sys.argv[1])
