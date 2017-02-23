import heapq
from collections import defaultdict

import numpy as np
import time

from copy import deepcopy

from real_utils import read_file, write_solution_to_file

ME_AT_THE_ZOO = "me_at_the_zoo.in"
EXAMPLE = "example.in"

# INPUT_FILE = ME_AT_THE_ZOO
INPUT_FILE = EXAMPLE


class AlgoBase(object):
    def __init__(self, max_iter):
        self.max_iter = max_iter
        self.solutions = {}

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

            # print 'curr state', current_state

            available_size = 100000
            for cs_id, videos in current_state.items():
                space_taken = 0
                for video in videos:
                    space_taken += self.size_by_video[video]
                if self.cache_size - space_taken < available_size:
                    available_size = self.cache_size - space_taken

            if available_size < self.smallest_video:
                # print 'SOLVED', current_state
                self.solutions[current_prio] = current_state

            for move in moves:
                if self._valid(current_state, move) and self._not_visited(current_state, move):
                    new_prio = self._get_new_prio(current_prio, move)
                    updated_state = self._get_updated_state(current_state, move)
                    heapq.heappush(states, (new_prio, updated_state))

        #     if solved:
        #         if self._first_solution() or self._better_solution(current_state):
        #             print 'Adding better solution, counter:', counter
        #             self._add_solution(current_state)
        #
            counter += 1


class VideoProblem(AlgoBase):
    def __init__(self, ep_by_ep_id, size_by_video, cs_ids, cache_size, eps_by_cs, max_iter):
        super(VideoProblem, self).__init__(max_iter=max_iter)
        self.ep_by_ep_id = ep_by_ep_id
        self.size_by_video = size_by_video
        self.cs_ids = cs_ids
        self.cache_size = cache_size
        self.eps_by_cs = eps_by_cs
        self.smallest_video = sorted(size_by_video.values())[0]
        self.visited_hashes = set()

    def _get_init_prio_and_state(self):
        videos_by_cs = defaultdict(list)
        # TODO: Tuple with a saved latency number? Is that the prio? Subtract the saved time from the prio (in secs)?
        initial_state = videos_by_cs
        return (100, initial_state)

    def _get_moves(self):
        moves = []
        for video_id in self.size_by_video.keys():
            for cs_id in self.cs_ids:
                moves.append((video_id, cs_id))
        return moves

    def _get_updated_state(self, current_state, move):
        video_id, cs_id = move
        new_state = deepcopy(current_state)
        new_state[cs_id].append(video_id)
        return new_state

    def _not_visited(self, current_state, move):
        hashable = tuple(current_state)
        h = hash(hashable)
        if h not in self.visited_hashes:
            self.visited_hashes.add(h)
            return False
        return True

    def _valid(self, current_state, move):
        video_id, cs_id = move

        if video_id in current_state[cs_id]:
            # Video already there
            return False

        currently_filled = 0
        for video_in_cache in current_state[cs_id]:
            currently_filled += self.size_by_video[video_in_cache]
        return currently_filled + self.size_by_video[video_id] <= self.cache_size

    def _get_new_prio(self, current_prio, move):
        video_id, cs_id = move
        time_saved = 0
        for ep in self.eps_by_cs[cs_id]:
            if video_id not in ep.requests_by_video:
                continue

            dc_latency = ep.dc_latency
            cs_latency = ep.latency_by_cs[cs_id]
            time_saved += (dc_latency - cs_latency) * ep.requests_by_video[video_id]
            time_saved = time_saved / -1000
        return time_saved


start_time = time.time()

ep_by_ep_id, size_by_video, cs_ids, cache_size, eps_by_cs = read_file(INPUT_FILE)
video_problem = VideoProblem(ep_by_ep_id, size_by_video, cs_ids, cache_size, eps_by_cs, max_iter=1000)
try:
    video_problem.run()
except KeyboardInterrupt:
    pass
finally:
    if len(video_problem.solutions.keys()) == 0:
        print 'NO SOLUTIONS FOUND'
    else:
        time_saved, sol = sorted(video_problem.solutions.items())[0]
        print sol
        write_solution_to_file(sol)

# ph_list = []
# solutions = []
# for index, ph in enumerate(ph_list):
#     # runner = PizzaRunner(ph, max_iter=50)
#     print('Running partition {}...').format(index+1)
#     # runner.run()
#     # solutions.append((ph, runner.solution()))
# unpack_solutions_and_write_file(solutions)

print
print 'Took {} second'.format(time.time() - start_time)
