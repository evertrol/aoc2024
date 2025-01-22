import re
import sys

text = ''.join(open(sys.argv[1]).read().split())
text2 = text[:]

pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
regex = re.compile(pattern)

total1 = total2 = 0
total1 = sum(
    int(match.group(1)) * int(match.group(2))
    for match in re.finditer(regex, text)
)

do = True
while text:
    if do:
        end = -1  # From where to start in memory for the next search
        # Search for a stop instruction
        m1 = text.find("don't")
        if m1 > -1:
            end = m1 + 5
        # Search for a multiplication instruction
        m2 = regex.search(text)
        if m2:
            # Test if the multiplication instruction
            # occurs before a stop instruction
            if m1 == -1 or m2.start() < m1:
                # Multiplication instruction first
                end = m2.end()
                x = int(m2.group(1))
                y = int(m2.group(2))
                total2 += x * y
            else:
                # Stop instruction occurrs first
                do = False
        if end == -1:
            # both patterns failed; no more relevant instructions
            break
        text = text[end:]
    else:
        # Find the continuation instruction
        m = text.find("do()")
        if m > -1:
            text = text[m+4:]
            do = True
        else:
            # If there is no continuation instruction,
            # this is the end of useful memory
            break
print(total1, total2)
exit()



pattern = r"(?:(?<=do\(\))|^).*?((?:mul\((\d{1,3}),(\d{1,3})\).*?)+)(?:(?=don't\(\))|$)"

#text2 = "mul(1,2)(*&^mul(3,4)}alksjdhfmul(1,2)"
#pattern = r"^(mul\((\d{1,3}),(\d{1,3})\).*?)+$"

#text2 = "5g5g3g2"
#pattern = r"((?P<digit>\d)g)+"
#pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
regex = re.compile(pattern)
match = regex.search(text2)
print(match.groups())
#print(match.groups(), match.group(0), match.group('digit'))
#print([match.group(1) for match in regex.finditer(text2)])
#print(reg.search(text2))

