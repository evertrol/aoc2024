from itertools import product, permutations
from operator import add, mul
import sys
	

def concat(left, right):
    return int(str(left) + str(right))


total1 = total2 = 0
for line in open(sys.argv[1]):
    test, inputs = line.split(':')
    test = int(test)
    inputs = list(map(int, inputs.strip().split()))

    valid = False
    for ops in product([add, mul], repeat=len(inputs) - 1):
        output = inputs[0]
        for op, value in zip(ops, inputs[1:]):
            output = op(output, value)
        if output == test:
            valid = True
            break
    if valid:
        total1 += test

    valid = False
    for ops in product([add, mul, concat], repeat=len(inputs) - 1):
        output = inputs[0]
        for op, value in zip(ops, inputs[1:]):
            output = op(output, value)
        if output == test:
            valid = True
            break
    if valid:
        total2 += test
print(total1, total2)
