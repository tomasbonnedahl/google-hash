import numpy as np
import itertools


def get_all_coord_combinations(rows, cols):
    coords = []
    for r in [row for row in xrange(rows+1)]:
        for c in [col for col in xrange(cols+1)]:
            coords.append((r, c))
    return list(itertools.combinations(coords, 2))


def make_it_work(pizza):
    updated_pizza = pizza.copy()
    return updated_pizza


def possible_slices(pizza):
    coord_combos = get_all_coord_combinations(pizza.shape[0], pizza.shape[1])

    for coord in coord_combos:
        start, finish = coord
        r_start, c_start = start
        r_finish, c_finish = finish

        # TODO: Rewrite with negating and not
        if r_start < r_finish and c_start < c_finish:
            a_slice = pizza[r_start:r_finish, c_start:c_finish]
            if a_slice.size >= 1 and a_slice.size <= 6:  # TODO: Not hardcoded...
                if a_slice.all():
                    # Checks that we are not slicing an already sliced part

                    slice_sum = np.sum(a_slice)
                    # Below checks both ingrediens and already taken parts of the pizza
                    if slice_sum > a_slice.size and slice_sum < 2*a_slice.size:  # TODO: Num of ingrediens is one here

                        updated_pizza = pizza.copy()
                        updated_pizza[r_start:r_finish, c_start:c_finish] = 0

                        yield (updated_pizza, start, finish, a_slice.size)
