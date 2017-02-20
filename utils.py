import datetime
import numpy as np


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


class PizzaHandler(object):
    def __init__(self, header):
        self.total_rows, self.total_cols, self.min_ing_per_slice, self.max_cells_per_slice = map(int, header)

    def add_pizza(self, pizza):
        self.pizza = pizza


def partition_pizza(big_ph):
    ph_list = []

    for i in xrange(0, 200, 20):
        for j in xrange(0, 250, 25):
            ph = PizzaHandler([20, 25, big_ph.min_ing_per_slice, big_ph.max_cells_per_slice])

            new_pizza = big_ph.pizza[i:i + ph.total_rows, j:j + ph.total_cols].copy()
            ph.add_pizza(new_pizza)

            ph.start_row = i
            ph.start_col = j
            ph_list.append(ph)

    return ph_list


def unpack_solutions_and_write_file(solutions):
    slices = []
    for ph, solution in solutions:
        _, solution_slices = solution
        for slice in solution_slices:
            start_row, start_col, end_row, end_col = slice
            start_row += ph.start_row
            start_col += ph.start_col
            end_row += ph.start_row
            end_col += ph.start_col
            slices.append((start_row, start_col, end_row, end_col))

    write_solution_to_file(slices)


def make_pizza_from_file(input_file):
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


def validate_slice_medium(slice, max_size_of_slice, min_ing_per_slice):
    slice_size = slice.size
    if slice_size < min_ing_per_slice*2 or slice_size > max_size_of_slice:
        return False

    if not slice.all():
        # Checks that we are not slicing an already sliced part - elements cannot be zero
        return False

    if not slice_within_ingredient_interval(slice, min_ing_per_slice=min_ing_per_slice):
        return False

    return True


def write_solution_to_file(slices):
    t = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
    # output_file_name = input_file_name.split('.')[0] + "-" + t + ".out"
    output_file_name = "medium-" + t + ".out"
    with open(output_file_name, 'w') as f:
        f.write('{}\n'.format(len(slices)))
        write_slices_to_file(f, slices)
    print
    print 'Solution written to:', output_file_name

def write_slices_to_file(f, solution_slices):
    for (r_start, c_start, r_finish, c_finish) in solution_slices:
        f.write('{} {} {} {}\n'.format(r_start, c_start, r_finish - 1, c_finish - 1))
