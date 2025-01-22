l,m=zip(*[map(int,l.split()) for l in open(0)])
print(sum(abs(i-j) for i,j in zip(sorted(l),sorted(m))),sum(n*m.count(n) for n in l))
