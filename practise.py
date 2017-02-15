import heapq

import numpy as np
import time

from utils import possible_slices, PrioHandler, write_to_file

EXAMPLE = "example.in"
SMALL = "small.in"

INPUT_FILE = EXAMPLE


"""
TODO
- Python3 for caching
- Check if generated coordinates is non-zero on pizza before
    creating a slice (possibly pre-mature optimisation)
"""


"""
0 = Already a slice
1 = Mushroom
2 = Tomato
"""

f_in = open(INPUT_FILE, 'r')
total_rows, total_cols, min_ing_per_slice, max_cells_per_slice = map(int, f_in.readline().rstrip().split())

pizza = np.ones((total_rows, total_cols), dtype=int)

for row_index, line in enumerate(f_in):
    for col_index, ingredient in enumerate(line.rstrip()):
        if ingredient == 'T':
            pizza[row_index][col_index] = 2


initial_state = (pizza, [])

states = []
initial_prio = 100000
heapq.heappush(states, (initial_prio, initial_state))

prio_handler = PrioHandler(max_cells_per_slice, init_prio=initial_prio)

slice_hashes_visited = set()

finished_work = []

start_time = time.time()

try:
    while states:
        old_prio, current_state = heapq.heappop(states)
        current_pizza, current_slices = current_state

        # If no possible slices found, consider this path to be solved
        slices_found = False

        for updated_pizza, (r_start, c_start), (r_finish, c_finish), slice_size in possible_slices(current_pizza,
                                                                                                   max_cells_per_slice,
                                                                                                   min_ing_per_slice):
            slices_found = True

            # Add the coordinates for the slice
            slices_coords = current_slices[:]
            slices_coords.append((r_start, c_start, r_finish, c_finish))

            slices_hashed = hash(tuple(sorted(slices_coords)))
            if slices_hashed not in slice_hashes_visited:
                new_prio = prio_handler.get_new_prio(old_prio, slice_size)

                slice_hashes_visited.add(slices_hashed)

                # Add the updated pizza to the queue with a new (unique) priority
                heapq.heappush(states, (new_prio, (updated_pizza, slices_coords)))

        if not slices_found:
            # Consider doing this outside later on to speed up the actual finding?
            if not finished_work:
                finished_work.append((current_pizza, current_slices))
            else:
                finished_pizza, finished_slices = finished_work[0]
                if np.count_nonzero(current_pizza) < np.count_nonzero(finished_pizza):
                    finished_work[0] = (current_pizza, current_slices)

except KeyboardInterrupt:
    pass

finally:
    for solution_pizza, solution_slices in finished_work:
        print 'SUCESS'
        print solution_pizza
        write_to_file(INPUT_FILE, solution_slices)

    print
    print 'Took {} second'.format(time.time()-start_time)