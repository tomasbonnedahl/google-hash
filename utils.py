import datetime
import numpy as np
import itertools

class PrioHandler(object):
    """
    This mess is needed as unique prios are required since the same prio will lead
    to comparing the second object which is the numpy array, which cannot be __cmp__.
    """
    def __init__(self, max_cells_per_slice, init_prio):
        self.max_cells_per_slice = max_cells_per_slice
        self.used_prios = set()
        self.used_prios.add(init_prio)

    def get_new_prio(self, old_prio, slice_size):
        # Calculate a new prio depending on the slices (the bigger the better)
        new_prio = old_prio - round(slice_size * 100.0 / self.max_cells_per_slice)
        while new_prio in self.used_prios:
            new_prio -= 1
        self.used_prios.add(new_prio)
        return new_prio


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

    # Tomato has value 2
    return slice.size + min_ing_per_slice <= slice_sum <= 2 * slice.size - min_ing_per_slice


def validate_slice(slice, max_size_of_slice, min_ing_per_slice):
    if slice.size < 1 or slice.size > max_size_of_slice:
        return False

    if not slice.all():
        # Checks that we are not slicing an already sliced part - elements cannot be zero
        return False

    if not slice_within_ingredient_interval(slice, min_ing_per_slice=min_ing_per_slice):
        return False

    return True

def write_to_file(input_file_name, solution_slices):
    t = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
    output_file_name = input_file_name.split('.')[0] + "-" + t + ".out"
    with open(output_file_name, 'w') as f:
        f.write('{}\n'.format(len(solution_slices)))
        for (r_start, c_start, r_finish, c_finish) in solution_slices:
            f.write('{} {} {} {}\n'.format(r_start, c_start, r_finish-1, c_finish-1))