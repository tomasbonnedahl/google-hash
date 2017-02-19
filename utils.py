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


def create_coords_medium(ph):
    # Min: 8, max 12
    """

    # First
    xxxx xxxx     (0,0 -> 0,9) # 8 really
    xxxx xxxxx    (0,0 -> 0,10)
    xxxxx xxxxx   (0,0 -> 0,11)
    xxxxx xxxxxx  (0,0 -> 0,12)
    xxxxxx xxxxxx (0,0 -> 0,13)

    # Second
    xxxx
    xxxx        (0,0 -> 2,5)
    xxxxx
    xxxxx       (0,0 -> 2,6)
    xxxxxx
    xxxxxx      (0,0 -> 2,7)

    # Third
    xxx
    xxx
    xxx         (0,0 -> 3,3)
    xxxx
    xxxx
    xxxx        (0,0 -> 3,4)

    # First (90)
    xxxxx
    xxxxx
    xxxxx
    xxxxx
    xxxxx
    xxxxx
    xxxxx
    xxxxx       (0,0 -> 9,0)
     xxxx       (0,0 -> 10,0)
      xxx       (0,0 -> 11,0)
       xx       (0,0 -> 12,0)
        x       (0,0 -> 13,0)

    # Second (90)
    xx
    xx
    xx
    xx          (0,0 -> 5,2)

    xx
    xx
    xx
    xx
    xx          (0,0 -> 6,2)

    xx
    xx
    xx
    xx
    xx
    xx          (0,0 -> 7,2)

    """
    for start_row in xrange(ph.pizza.shape[0]):
        for start_col in xrange(ph.pizza.shape[1]-2*ph.min_ing_per_slice+1):
            # First scenario
            for i in xrange(ph.min_ing_per_slice*2, ph.max_cells_per_slice+1):
                end_row = start_row + 1
                end_col = start_col + i
                yield (start_row, start_col, end_row, end_col)
                yield (start_row, start_col, end_col, end_row)

    for start_row in xrange(ph.pizza.shape[0]-1):
        for start_col in xrange(ph.pizza.shape[1]-3):
            # Second scenario
            for i in xrange(ph.min_ing_per_slice, ph.min_ing_per_slice+3):
                end_row = start_row + 2
                end_col = start_col + i
                yield (start_row, start_col, end_row, end_col)
                yield (start_row, start_col, end_col, end_row)

    for start_row in xrange(ph.pizza.shape[0] - 2):
        for start_col in xrange(ph.pizza.shape[1] - 2):
            # Third scenario
            for i in xrange(3, 5):
                end_row = start_row + 3
                end_col = start_col + i
                yield (start_row, start_col, end_row, end_col)
                yield (start_row, start_col, end_col, end_row)


def validate_possible_slices_medium(pizza, coords, ph):
    start_row, start_col, end_row, end_col = coords
    if end_row > ph.total_rows or end_col > ph.total_cols:
        return False

    a_slice = pizza[start_row:end_row, start_col:end_col]
    return validate_slice_medium(a_slice, ph.max_cells_per_slice, ph.min_ing_per_slice)


def slice_within_ingredient_interval(slice, min_ing_per_slice):
    slice_sum = np.sum(slice)

    # Tomato has value 2
    return slice.size + min_ing_per_slice <= slice_sum <= 2 * slice.size - min_ing_per_slice


def validate_slice(slice, max_size_of_slice, min_ing_per_slice):
    # TODO: Remove
    slice_size = slice.size
    if slice_size < 1 or slice_size > max_size_of_slice:
        return False

    if not slice.all():
        # Checks that we are not slicing an already sliced part - elements cannot be zero
        return False

    if not slice_within_ingredient_interval(slice, min_ing_per_slice=min_ing_per_slice):
        return False

    return True


def validate_slice_medium(slice, max_size_of_slice, min_ing_per_slice):
    # TODO: Remove check against size
    slice_size = slice.size
    if slice_size < min_ing_per_slice*2 or slice_size > max_size_of_slice:
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