import sys

rules = {}
updates = []
for line in open(sys.argv[1]):
    if '|' in line:
        x, y = map(int, line.split('|'))
        rules.setdefault(x, set()).add(y)
    elif ',' in line:
        updates.append([int(x) for x in line.split(',')])
    
total1 = 0
total2 = 0
for update in updates:
    n = len(update)
    nswaps = 0
    while True:
        for i in range(n):
            before = set(update[:i])
            m = update[i]
            # Match the before set with all values that should follow after
            k = rules.get(m, set()) & before
            if k:
                # Pick a random value out of the 'should follow after' list
                # And find its position in the update
                j = update.index(k.pop())
                # and swap this with the current value
                update[i], update[j] = update[j], update[i]
                nswaps += 1
                # Break and check the full list again with the new ordering
                break
        else:  # correct
            break
    if nswaps == 0:
        total1 += update[n//2]
    else:
        total2 += update[n//2]
print(total1, total2)
