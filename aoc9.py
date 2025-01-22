import sys


data = list(map(int, open(sys.argv[1]).read().strip()))
data2 = data.copy()

checksum = 0
idleft = 0
idright = len(data) // 2 + 1
i = 0
j = len(data) + 1
pos = 0
right = 0
new = []
while i <= j:
    if i >= j:
        for _ in range(right):
            checksum += idleft * pos
            new.append(idleft)
            pos += 1
        break
    for _ in range(data[i]):
        checksum += idleft * pos
        new.append(idleft)
        pos += 1
    i += 1
    idleft += 1
    while idright >= idleft:
        if right >= data[i]:
            for _ in range(data[i]):
                checksum += idright * pos
                new.append(idright)
                pos += 1
            right -= data[i]
            i += 1
            break
        else: # right < data[i]
            for _ in range(right):#data[i]):
                checksum += idright * pos
                new.append(idright)
                pos += 1
            data[i] -= right
            j -= 2
            right = data[j]
            idright -= 1

print(checksum)

data = data2

x = 0
pos = [0] + [x := x + value for value in data]
empty = {p: n for p, n in zip(pos[1::2], data[1::2])}
items = {p: n for p, n in zip(pos[::2], data[::2])}
ids = {p: id for p, id in zip(pos[::2], range(len(data) // 2 + 1))}

keys = list(reversed(items.keys()))
for key in keys:
    value = items[key]
    emptypos = sorted(empty.keys())
    for pos in emptypos:
        gap = empty[pos]
        if pos > key:
            break
        if value <= gap:
            id = ids.pop(key)
            del items[key]
            items[pos] = value
            ids[pos] = id
            rest = gap - value
            if rest:
                empty[pos+value] = rest
            del empty[pos]
            break
assert set(items.keys()) == set(ids.keys())
checksum = 0
for pos, value in items.items():
    for i in range(value):
        checksum += ids[pos] * (pos + i)
print(checksum)
