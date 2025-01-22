import sys


def combo(op, register):
    if op == 7:
        raise ValueError
    if 0 <= op <= 3:
        return op
    return register[op - 4]


def adv(op, register):
    rval = combo(op, register)
    rval = 2**rval
    # rval = 1 << rval
    register[0] = register[0] // rval
    register[3] += 2


def bxl(op, register):
    register[1] = register[1] ^ op
    register[3] += 2


def bst(op, register):
    register[1] = combo(op, register) % 8
    register[3] += 2


def jnz(op, register):
    if register[0]:
        register[3] = op
    else:
        register[3] += 2


def bxc(op, register):
    register[1] = register[1] ^ register[2]
    register[3] += 2


def out(op, register):
    value = combo(op, register) % 8
    register[3] += 2
    return value


def bdv(op, register):
    rval = combo(op, register)
    rval = 2**rval
    register[1] = register[0] // rval
    register[3] += 2


def cdv(op, register):
    rval = combo(op, register)
    rval = 2**rval
    register[2] = register[0] // rval
    register[3] += 2


ops = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv,
}


def read(fname):
    register = {}
    with open(fname) as fp:
        for line in fp:
            if line == "\n":  # empty line
                continue
            key, value = line.split(":")
            if "A" in key:
                register[0] = int(value)
            elif "B" in key:
                register[1] = int(value)
            if "C" in key:
                register[2] = int(value)
            if "P" in key:
                values = list(map(int, value.split(",")))
    return register, values


def calc(register, values):
    results = []
    while True:
        try:
            op = values[register[3]]
            value = values[register[3] + 1]
        except IndexError:
            # past end of program: halt
            break
        result = ops[op](value, register)
        if result is not None:
            results.append(result)
    return results


def calculate(offset, index, basereg, values):
    aa = list(range(offset, offset + 8))
    value = 0
    for j, a in enumerate(aa):
        # skip a == 0, since 8*a == 0 in the recursing call,
        # resulting in the same loop over and over
        if a == 0:
            continue
        register = basereg.copy()
        register[0] = a
        results = calc(register, values)
        if results[-index - 1 :] == values[-index - 1 :]:
            if results == values:
                return a
            value = calculate(8 * a, index + 1, basereg, values)
            if value:
                break
    return value


register, values = read(sys.argv[1])
register[3] = 0
results = calc(register.copy(), values)
value = calculate(0, 0, register, values)
print(",".join(str(result) for result in results), value)
