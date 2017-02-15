import numpy as np
import itertools

import functools

ROWS = 3
COLS = 5

pizza = np.ones((ROWS, COLS), dtype=int)

for x in xrange(1, 4):
    pizza[1][x] = 0

# print 'row', pizza[1,:] # Row
# print 'col', pizza[:,1] # Col
# print 'upper left corner:'
# print pizza[0:2,0:2] # Upper left corner, 2x2

print 'whole:'
print pizza[0:pizza.shape[0], 0:pizza.shape[1]]
pizza[0:3, 0:2] = 0
print pizza

l = [2,3,1]
l += [4]
print l
s = sorted(l)
print 's', s
t = tuple(s)
print 't', t
h = hash(t)
print 'h', h

# t = (('asf'), 123)
# t = t + (1,)
#
# print 't', t
# # s = sorted(t)
# # print 'sort', s, type(s)
# print hash(t)