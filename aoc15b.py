import sys


grid = {}
walls = set()
boxes, lboxes, rboxes = set(), set(), set()
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
    xmax = 2 * len(line)
    x = 0
    for char in line:
        if char == '@':
            player = (x, y)
            grid[(x, y)] = '@'
        elif char == 'O':
            boxes.add((x, y))
            lboxes.add((x, y))
            grid[(x, y)] = '['
            rboxes.add((x+1, y))
            grid[(x+1, y)] = ']'
        elif char == '#':
            walls.add((x, y))
            grid[(x, y)] = '#'
            walls.add((x+1, y))
            grid[(x+1, y)] = '#'
        elif char == '.':
            pass
        else:
            grid[(x, y)] = '?'
            print(f'unknown {char = } at pos = ({x}, {y})')
        x += 2

size = xmax, ymax
moves = ''.join(moves)

def testleft(walls, boxes, pos, size, oldboxes, boxesmove):
    x, y = pos
    test = x - 1, y
    test2 = x - 2, y
    if test in walls:
        return False
    if test2 in boxes:
        oldboxes.add(pos)
        boxesmove.add(test2)
        return testleft(walls, boxes, test2, oldboxes, boxesmove)
    return True

def testup(walls, boxes, pos, oldboxes, boxesmove, player):
    x, y = pos
    test = x, y - 1
    testl = x - 1, y - 1
    testr = x + 1, y - 1
    ok1 = ok2 = ok3 = True

    if test in walls:
        oldboxes, boxesmove = set(), set()
        return False
    if pos != player and testr in walls:
        oldboxes, boxesmove = set(), set()
        return False
    oldboxes.add(pos)
    boxesmove.add(test)
    if test in boxes:
        ok1 = testup(walls, boxes, test, oldboxes, boxesmove, player)

    if testl in boxes:
        ok2 = testup(walls, boxes, testl, oldboxes, boxesmove, player)
    if pos == player:
        return ok1 and ok2
    if testr in boxes:
        ok3 = testup(walls, boxes, testr, oldboxes, boxesmove, player)
    return ok1 and ok2 and ok3


def testdown(walls, boxes, pos, oldboxes, boxesmove, player):
    x, y = pos
    test = x, y + 1
    testl = x - 1, y + 1
    testr = x + 1, y + 1
    ok1 = ok2 = ok3 = True

    if test in walls:#
        oldboxes, boxesmove = set(), set()
        return False
    if pos != player and testr in walls:
        oldboxes, boxesmove = set(), set()
        return False
    oldboxes.add(pos)
    boxesmove.add(test)
    if test in boxes:
        ok1 = testdown(walls, boxes, test, oldboxes, boxesmove, player)

    if testl in boxes:
        ok2 = testdown(walls, boxes, testl, oldboxes, boxesmove, player)
    if pos == player:
        return ok1 and ok2
    if testr in boxes:
        ok3 = testdown(walls, boxes, testr, oldboxes, boxesmove, player)
    return ok1 and ok2 and ok3


for imove, move in enumerate(moves):
    boxesmove = lboxesmove = rboxesmove = None
    if move == '^':
        xp, yp = player
        new = xp, yp - 1
        nomove = False
        oldboxes = set()
        boxesmove = set()
        oldboxes, boxesmove = set(), set()
        ob, bx = set(), set()
        ok = testup(walls, boxes, player, oldboxes, boxesmove, player)
        if ok:
            oldboxes.discard(player)
            boxesmove.discard(new)
        else:
            nomove = True
    elif move == 'v':
        xp, yp = player
        new = xp, yp + 1
        nomove = False
        oldboxes = set()
        boxesmove = set()
        ok = testdown(walls, boxes, player, oldboxes, boxesmove, player)
        if ok:
            oldboxes.discard(player)
            boxesmove.discard(new)
        else:
            nomove = True
    elif move == '<':
        xp, yp = player
        new = xp - 1, yp
        nomove = False
        oldboxes, boxesmove = set(), set()
        oldlboxes, oldrboxes = set(), set()
        lboxesmove, rboxesmove = set(), set()
        x = xp
        while x >= 0:
            cur = x, yp
            test = x - 1, yp
            if test in walls:
                nomove = True
                break
            test = x - 2, yp
            if test in boxes:
                oldboxes.add(test)
                boxesmove.add((test[0] - 1, yp))
                x -= 2
            else:
                break
    elif move == '>':
        xp, yp = player
        new = xp + 1, yp
        nomove = False
        oldboxes, boxesmove = set(), set()
        oldlboxes, oldrboxes = set(), set()
        lboxesmove, rboxesmove = set(), set()
        x = xp
        while x <= xmax:
            cur = x, yp
            test = x + 1, yp
            if test in walls:
                nomove = True
                break
            if test in boxes:
                oldboxes.add(test)
                boxesmove.add((test[0] + 1, yp))
                x += 2
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
