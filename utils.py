import numpy as np
import itertools


def get_all_coord_combinations(rows, cols):
    coords = []
    for r in [row for row in xrange(rows+1)]:
        for c in [col for col in xrange(cols+1)]:
            coords.append((r, c))
    return list(itertools.combinations(coords, 2))


def possible_slices(pizza, max_size_of_slice, min_ing_per_slice):
    coord_combos = get_all_coord_combinations(pizza.shape[0], pizza.shape[1])

    for coord in coord_combos:
        start, finish = coord
        r_start, c_start = start
        r_finish, c_finish = finish

        if r_start >= r_finish or c_start >= c_finish:
            continue

        a_slice = pizza[r_start:r_finish, c_start:c_finish]
        if not validate_slice(a_slice, max_size_of_slice, min_ing_per_slice):
            continue

        # Update the pizza with the new slice
        updated_pizza = pizza.copy()
        updated_pizza[r_start:r_finish, c_start:c_finish] = 0

        yield (updated_pizza, start, finish, a_slice.size)


def slice_within_ingredient_interval(slice, min_ing_per_slice):
    slice_sum = np.sum(slice)
    return slice.size + min_ing_per_slice <= slice_sum <= 2 * slice.size - min_ing_per_slice # Tomato has value 2


def validate_slice(slice, max_size_of_slice, min_ing_per_slice):
    if slice.size < 1 or slice.size > max_size_of_slice:
        return False

    if not slice.all():
        # Checks that we are not slicing an already sliced part - elements cannot be zero
        return False

    if not slice_within_ingredient_interval(slice, min_ing_per_slice=min_ing_per_slice):
        return False

    return True

"""
Each slice to have 2 of the ing
A slice with size 4 should have 2T and 2M -> 2*1 + 2*2 = 6
If it only has 4T -> 4*1 = 4 < slice.size

If one ing per slice
Slice is 2 -> Must be between 3 and 3 (not 2 or 4)
Slice is 4 -> Must be between 5 and 7 (not 4 or 8)

If two ing per slice
Slice is 4 -> Must be between 6 and 6 (not 5 or 7)
Slice (size) is 6 -> Must be between 8 and 10 (not 7 or 11)

ing_per_slice + 2*ing_per_slice <= slice_size < only T's


x = minimum sum it can have is its size (only 1s)
x + minim_ing*2 <= sum



"""