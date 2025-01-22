# Day 1 is the only script that reads from stdin, to be smaller
printf "AoC day 1:  "
python aoc1.py < aoc1.in
for i in {2..12}
do
	printf "Day $i:  "
	python aoc${i}.py aoc${i}.in
done
# Day 12 is missing
printf "AoC day 13:  "
python aoc13.py aoc13.in
echo "Day 14:"  # Prints Christmas tree as well
python aoc14.py aoc14.in
printf "Day 15, part 1:  "
# Day 15 is split into two separate scripts
python aoc15a.py aoc15.in
printf "Day 15, part 2:  "
python aoc15b.py aoc15.in

for i in {16..17}
do
	printf "Day $i:  "
	python aoc${i}.py aoc${i}.in
done
