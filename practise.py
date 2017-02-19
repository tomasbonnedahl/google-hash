import heapq

import numpy as np
import time

from utils import PrioHandler, write_to_file, create_coords_medium, validate_possible_slices_medium

EXAMPLE = "example.in"
SMALL = "small.in"
MEDIUM = "medium.in"
MEDIUM_TEST = "medium-test.in"

INPUT_FILE = MEDIUM_TEST


"""
0 = Already a slice
1 = Mushroom
2 = Tomato
"""


class PizzaHandler(object):
    def __init__(self, header):
        self.total_rows, self.total_cols, self.min_ing_per_slice, self.max_cells_per_slice = map(int, header)

    def add_pizza(self, pizza):
        self.pizza = pizza


def make_pizza(input_file):
    f_in = open(input_file, 'r')
    header = map(int, f_in.readline().rstrip().split())
    ph = PizzaHandler(header)

    pizza = np.ones((ph.total_rows, ph.total_cols), dtype=int)
    for row_index, line in enumerate(f_in):
        for col_index, ingredient in enumerate(line.rstrip()):
            if ingredient == 'T':
                pizza[row_index][col_index] = 2
    ph.add_pizza(pizza)
    return ph


ph = make_pizza(INPUT_FILE)

# Setup the queue
initial_state = (ph.pizza, [])
states = []
initial_prio = 100000
heapq.heappush(states, (initial_prio, initial_state))
prio_handler = PrioHandler(ph.max_cells_per_slice, init_prio=initial_prio)
slice_hashes_visited = set()
finished_work = []


start_time = time.time()

all_coords = []
for coords in create_coords_medium(ph):
    all_coords.append(coords)


try:
    while states:
        old_prio, current_state = heapq.heappop(states)
        current_pizza, current_slices = current_state

        # If no possible slices found, consider this path to be solved
        slices_found = False

        for coords in all_coords:
            r_start, c_start, r_finish, c_finish = coords

            if validate_possible_slices_medium(current_pizza, coords, ph):
                # Update the pizza with the new slice
                updated_pizza = current_pizza.copy()
                updated_pizza[r_start:r_finish, c_start:c_finish] = 0

                slices_found = True

                # Add the coordinates for the slice
                slices_coords = current_slices[:]
                slices_coords.append(coords)

                slices_hashed = hash(tuple(sorted(slices_coords)))
                if slices_hashed not in slice_hashes_visited:
                    slice_size = (r_finish - r_start) * (c_finish - c_finish)
                    new_prio = prio_handler.get_new_prio(old_prio, slice_size)
                    slice_hashes_visited.add(slices_hashed)

                    # Add the updated pizza to the queue with a new (unique) priority
                    heapq.heappush(states, (new_prio, (updated_pizza, slices_coords)))

        if not slices_found:
            # Consider doing this outside later on to speed up the actual finding?
            if not finished_work:
                print 'Adding first solution'
                finished_work.append((current_pizza, current_slices))
            else:
                finished_pizza, finished_slices = finished_work[0]
                if np.count_nonzero(current_pizza) < np.count_nonzero(finished_pizza):
                    print 'Adding better solution'
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