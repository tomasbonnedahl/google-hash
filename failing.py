import heapq
import numpy as np

a = np.ones((2, 2), dtype=int)

states = []
heapq.heappush(states, (0, a))
heapq.heappush(states, (1, a.copy()))

# import Queue as Q
#
# q = Q.PriorityQueue()
# q.put((1, a))
# q.put((1, a.copy()))
# while not q.empty():
#     print q.get()
#     print