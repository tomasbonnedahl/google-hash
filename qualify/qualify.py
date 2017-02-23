import heapq

import numpy as np
import time

from qualify_utils import read_file

EXAMPLE = "example.in"
SMALL = "small.in"
MEDIUM = "medium.in"
MEDIUM_TEST = "medium-test.in"

INPUT_FILE = EXAMPLE


class AlgoBase(object):
    def __init__(self, max_iter):
        self.max_iter = max_iter

    def _get_init_prio_and_state(self):
        raise NotImplementedError()

    def _get_moves(self):
        raise NotImplementedError()

    def _valid(self, current_state, move):
        raise NotImplementedError()

    def _not_visited(self, current_state, move):
        raise NotImplementedError()

    def _get_new_prio(self, current_prio, move):
        raise NotImplementedError()

    def _get_updated_state(self, current_state, move):
        raise NotImplementedError()

    def _first_solution(self):
        raise NotImplementedError()

    def _better_solution(self, current_state):
        raise NotImplementedError()

    def _add_solution(self, current_state):
        raise NotImplementedError()

    def solution(self):
        raise NotImplementedError()

    def run(self):
        states = []
        heapq.heappush(states, self._get_init_prio_and_state())

        moves = self._get_moves()

        counter = 0
        while states and counter < self.max_iter:
            current_prio, current_state = heapq.heappop(states)

            solved = True

            for move in moves:
                if self._valid(current_state, move) and self._not_visited(current_state, move):
                    solved = False

                    new_prio = self._get_new_prio(current_prio, move)
                    heapq.heappush(states, (new_prio, self._get_updated_state(current_state, move)))

            if solved:
                if self._first_solution() or self._better_solution(current_state):
                    print 'Adding better solution, counter:', counter
                    self._add_solution(current_state)

            counter += 1


# class PizzaRunner(AlgoBase):
#     def __init__(self, ph, max_iter):
#         self.ph = ph
#         self.slice_hashes_visited = set()
#         self.initial_prio = 100000
#         self.prio_handler = PrioHandler(ph.max_cells_per_slice, init_prio=self.initial_prio)
#         self.finished_work = None
#         super(PizzaRunner, self).__init__(max_iter=max_iter)
#
#     def _get_init_prio_and_state(self):
#         initial_state = (ph.pizza, [])
#         return (self.initial_prio, initial_state)
#
#     def _get_moves(self):
#         all_coords = []
#         for coords in create_coords_medium(ph):
#             all_coords.append(coords)
#         return all_coords
#
#     def _valid(self, current_state, move):
#         current_pizza, current_slices = current_state
#         return validate_possible_slices_medium(current_pizza, move, self.ph)
#
#     def _not_visited(self, current_state, move):
#         current_pizza, current_slices = current_state
#         self.slices_coords = current_slices[:]
#         self.slices_coords.append(move)
#         slices_hashed = hash(tuple(sorted(self.slices_coords)))
#         visited = slices_hashed in self.slice_hashes_visited
#
#         if not visited:
#             self.slice_hashes_visited.add(slices_hashed)
#
#         return not visited
#
#     def _get_new_prio(self, current_prio, move):
#         r_start, c_start, r_finish, c_finish = move
#         slice_size = (r_finish - r_start) * (c_finish - c_finish)
#         return self.prio_handler.get_new_prio(current_prio, slice_size)
#
#     def _get_updated_state(self, current_state, move):
#         current_pizza, current_slices = current_state
#         r_start, c_start, r_finish, c_finish = move
#         updated_pizza = current_pizza.copy()
#         updated_pizza[r_start:r_finish, c_start:c_finish] = 0
#         return (updated_pizza, self.slices_coords)
#
#     def _first_solution(self):
#         return self.finished_work is None
#
#     def _better_solution(self, current_state):
#         current_pizza, _ = current_state
#         finished_pizza, finished_slices = self.finished_work
#         return np.count_nonzero(current_pizza) < np.count_nonzero(finished_pizza)
#
#     def _add_solution(self, current_state):
#         self.finished_work = current_state
#
#     def solution(self):
#         return self.finished_work


start_time = time.time()

big_ph = read_file(INPUT_FILE)
# ph_list = partition_pizza(big_ph)
ph_list = []

solutions = []

for index, ph in enumerate(ph_list):
    # runner = PizzaRunner(ph, max_iter=50)
    print('Running partition {}...').format(index+1)
    # runner.run()
    # solutions.append((ph, runner.solution()))

# unpack_solutions_and_write_file(solutions)

print
print 'Took {} second'.format(time.time() - start_time)
