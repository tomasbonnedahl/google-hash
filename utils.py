import numpy as np
import itertools


def get_all_coord_combinations(rows, cols):
    coords = []
    for r in [row for row in xrange(rows+1)]:
        for c in [col for col in xrange(cols+1)]:
            coords.append((r, c))
    return list(itertools.combinations(coords, 2))


def possible_slices(pizza):
    coord_combos = get_all_coord_combinations(pizza.shape[0], pizza.shape[1])

    for coord in coord_combos:
        start, finish = coord
        r_start, c_start = start
        r_finish, c_finish = finish

        if r_start >= r_finish or c_start >= c_finish:
            continue

        a_slice = pizza[r_start:r_finish, c_start:c_finish]
        if a_slice.size < 1 or a_slice.size > 6:  # TODO: Not hardcoded...
            continue

        if not a_slice.all():
            # Checks that we are not slicing an already sliced part - elements cannot be zero
            continue

        slice_sum = np.sum(a_slice)

        # TODO: Num of each ingredient per slice is one here
        if slice_sum <= a_slice.size or slice_sum >= 2*a_slice.size:
            continue

        # Update the pizza with the new slice
        updated_pizza = pizza.copy()
        updated_pizza[r_start:r_finish, c_start:c_finish] = 0

        yield (updated_pizza, start, finish, a_slice.size)
