from functools import cache
import sys


@cache
def calculate(x, n, level=25):
    if level == 0:
        return 1
    if x == '0':
        n = calculate('1', n, level-1)
    elif len(x) % 2 == 0:
        m = len(x)
        n = calculate(x[:m//2], n, level-1)
        n += calculate(str(int(x[m//2:])), n, level-1)
    else:
        n = calculate(str(2024 * int(x)), n, level-1)
    return n


data = open(sys.argv[1]).read().strip().split()
print(sum(calculate(x, 0) for x in data), sum(calculate(x, 0, level=75) for x in data))
