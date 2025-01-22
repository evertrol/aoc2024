import sys

def search1(pos, grid):    
    x, y = pos
    words = [''] * 8
    for i in range(4):
        words[0] += grid[(x+i, y)]
        words[1] += grid[(x-i, y)]
        words[2] += grid[(x, y+i)]
        words[3] += grid[(x, y-i)]
        words[4] += grid[(x+i, y+i)]
        words[5] += grid[(x-i, y+i)]
        words[6] += grid[(x+i, y-i)]
        words[7] += grid[(x-i, y-i)]
    return words.count('XMAS')


def search2(pos, grid):
    x, y = pos
    letters = grid[x-1, y-1] + grid[x+1, y+1]
    if letters == 'MS' or letters == 'SM':
        letters = grid[x-1, y+1] + grid[x+1, y-1]
        if letters == 'MS' or letters == 'SM':
            return True
    return False


lines = open(sys.argv[1]).read().strip().split('\n')
ymax, xmax = len(lines), len(lines[0])
border = 5
grid = {}
for y in range(-border, ymax+border):
    for x in range(-border, xmax+border):
        grid[(x, y)] = ''
for y, line in enumerate(lines):
    for x, letter in enumerate(line):
        grid[(x, y)] = letter
        
total1 = total2 = 0
for key, letter in grid.items():
    if letter == 'X':
        total1 += search1(key, grid)
    if letter == 'A':
        total2 += search2(key, grid)
print(total1, total2)
