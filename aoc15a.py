import sys


grid = {}
walls = set()
boxes = set()
moves = []
read_moves = False
for y, line in enumerate(open(sys.argv[1])):
    line = line.strip()
    if not line:
        ymax = y
        read_moves = True
        continue
    if read_moves:
        moves.append(line)
        continue
    xmax = len(line)
    for x, char in enumerate(line):
        if char == '@':
            player = (x, y)
            grid[(x, y)] = '@'
        elif char == 'O':
            boxes.add((x, y))
            grid[(x, y)] = 'O'
        elif char == '#':
            walls.add((x, y))
            grid[(x, y)] = '#'
        elif char == '.':
            pass
        else:
            grid[(x, y)] = '?'
            print(f'unknown {char = } at pos = ({x}, {y})')

size = xmax, ymax
moves = ''.join(moves)
for imove, move in enumerate(moves):
    if move == '^':
        xp, yp = player
        new = xp, yp - 1
        nomove = False
        oldboxes = set()
        boxesmove = set()
        for y in range(yp, 0, -1):
            cur = xp, y
            test = xp, y - 1
            if test in walls:
                nomove = True
                break
            elif test in boxes:
                oldboxes.add(test)
                boxesmove.add((xp, test[1] - 1))
            else:
                break
    elif move == 'v':
        xp, yp = player
        new = xp, yp + 1
        nomove = False
        oldboxes = set()
        boxesmove = set()
        for y in range(yp, ymax+1):
            cur = xp, y
            test = xp, y + 1
            if test in walls:
                nomove = True
                break
            elif test in boxes:
                oldboxes.add(test)
                boxesmove.add((xp, test[1] + 1))
            else:
                break
    elif move == '<':
        xp, yp = player
        new = xp - 1, yp
        nomove = False
        oldboxes = set()
        boxesmove = set()
        for x in range(xp, 0, -1):
            cur = x, yp
            test = x - 1, yp
            if test in walls:
                nomove = True
                break
            elif test in boxes:
                oldboxes.add(test)
                boxesmove.add((test[0] - 1, yp))
            else:
                break
    elif move == '>':
        xp, yp = player
        new = xp + 1, yp
        nomove = False
        oldboxes = set()
        boxesmove = set()
        for x in range(xp, xmax+1):
            cur = x, yp
            test = x + 1, yp
            if test in walls:
                nomove = True
                break
            elif test in boxes:
                oldboxes.add(test)
                boxesmove.add((test[0] + 1, yp))
            else:
                break

    if nomove:
        continue
    elif boxesmove:
        assert len(boxesmove) == len(oldboxes)
        boxes -= oldboxes
        boxes |= boxesmove
    player = new

gps = 0
for box in boxes:
    gps += box[0] + 100 * box[1]
print(gps)
