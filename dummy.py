import numpy as np
import itertools

import functools

from utils import create_coords_medium

ROWS = 3
COLS = 5

pizza = np.ones((ROWS, COLS), dtype=int)

for x in xrange(1, 4):
    pizza[1][x] = 0

# print 'row', pizza[1,:] # Row
# print 'col', pizza[:,1] # Col
# print 'upper left corner:'
# print pizza[0:2,0:2] # Upper left corner, 2x2

# a = np.arange(225).reshape(15, 15)
a = np.arange(100).reshape(10, 10)
# print a

print a[0:5, 0:5]
print a[0:5, 5:]

t = (1, 2, 3)
a, b, c = map(lambda x: x+1, t)
print 'c', c