from collections import defaultdict

t = ((1,2), (3,4), (5,6))
# t = tuple(() for x in xrange(3))
print t, type(t), len(t)

l = list(t)
print l[1], type(l[1])
new_l = list(l[1])
new_l.append(666)
new_t = tuple(new_l)
print 'afasfs', new_t

print 't[1]:', t[1]

d = {0: (1, 2, 3), 1: (4, 5, 6)}
print 'tup', tuple(d.items())

d2 = defaultdict(tuple)
print d2
t = list(d2[0])
t.append(123)
print t
d2[0] = tuple(t)
print d2

t = list(d2[0])
t.append(666)
print t
d2[0] = tuple(t)
print d2

t = list(d2[1])
t.append(555)
print t
d2[1] = tuple(t)
print d2

