from itertools import pairwise, starmap
from operator import gt
import sys


def testsafe(items):
    incr = items[1] > items[0]
    return (all((i > j) == incr for i, j in zip(items[1:], items[:-1])) and
            all(0 < abs(i-j) < 4 for i, j in zip(items[1:], items[:-1])))

total1 = total2 = 0
for line in open(sys.argv[1]):
    items = list(map(int, line.split()))
    if testsafe(items):
        total1 += 1
        continue
    for i in range(len(items)):
        tmpitems = items[:]
        tmpitems.pop(i)
        if testsafe(tmpitems):
            total2 += 1
            break
print(total1, total1 + total2)
