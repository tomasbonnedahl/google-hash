import heapq
from collections import defaultdict

import time

from copy import deepcopy

from real_utils import read_file, write_solution_to_file

EXAMPLE = "example.in"
ME_AT_THE_ZOO = "me_at_the_zoo.in"
VIDEOS_WORTH_SPREADING = 'videos_worth_spreading.in'

INPUT_FILE = VIDEOS_WORTH_SPREADING


class AlgoBase(object):
    def __init__(self, max_iter):
        self.max_iter = max_iter
        self.solutions = {}

    def _get_init_prio_and_state(self):
        raise NotImplementedError()

    def _get_moves(self):
        raise NotImplementedError()

    def _valid(self, current_videos_by_cs, current_capacity_by_cs, move):
        raise NotImplementedError()

    def _visited(self, current_state):
        raise NotImplementedError()

    def _get_new_prio(self, current_prio, videos_distributed, move):
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

        counter = 0
        while states and counter < self.max_iter:
            current_prio, current_data = heapq.heappop(states)
            current_videos_by_cs, current_capacity_by_cs, videos_distributed = current_data

            solved = True
            for move in self._get_moves():
                if self._valid(current_videos_by_cs, current_capacity_by_cs, move):
                    updated_state = self._get_updated_state(current_data, move)
                    updated_videos_by_cs, updated_capacity_by_cs, updated_videos_distributed = updated_state
                    if not self._visited(updated_videos_by_cs):
                        solved = False
                        new_prio = self._get_new_prio(current_prio, updated_videos_distributed, move)
                        heapq.heappush(states, (new_prio, updated_state))

            if solved:
                print 'SOLVED'
                self.solutions[current_prio] = current_videos_by_cs

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
        videos_by_cs = defaultdict(tuple)
        capacity_by_cs = [0 for x in xrange(len(self.cs_ids))]
        videos_distributed = 0
        initial_state = (videos_by_cs, capacity_by_cs, videos_distributed)
        return (0, initial_state)

    def _get_moves(self):
        for video_id in self.size_by_video.keys():
            for cs_id in self.cs_ids:
                yield (video_id, cs_id)

    def _get_updated_state(self, current_data, move):
        video_id, cs_id = move
        videos_by_cs, capacity_by_cs, videos_distributed = current_data

        new_current_videos_by_cs = deepcopy(videos_by_cs)  # TODO: Needed?
        item = list(new_current_videos_by_cs[cs_id])
        item.append(video_id)
        new_current_videos_by_cs[cs_id] = tuple(item)

        new_capacity_by_cs = deepcopy(capacity_by_cs)
        new_capacity_by_cs[cs_id] += self.size_by_video[video_id]

        new_state = (new_current_videos_by_cs, new_capacity_by_cs, videos_distributed+1)
        return new_state

    def _visited(self, current_videos_by_cs):
        h = hash(tuple(current_videos_by_cs.items()))
        if h not in self.visited_hashes:
            self.visited_hashes.add(h)
            return False
        return True

    def _valid(self, current_videos_by_cs, current_capacity_by_cs, move):
        video_id, cs_id = move

        if video_id in current_videos_by_cs[cs_id]:
            # Video already there
            return False
        return current_capacity_by_cs[cs_id] + self.size_by_video[video_id] <= self.cache_size

    def _get_new_prio(self, current_prio, videos_distributed, move):
        video_id, cs_id = move
        time_saved = 0
        for ep in self.eps_by_cs[cs_id]:
            if video_id not in ep.requests_by_video:
                continue

            dc_latency = ep.dc_latency
            cs_latency = ep.latency_by_cs[cs_id]
            time_saved += (dc_latency - cs_latency) * ep.requests_by_video[video_id] / 1000
        return (current_prio - time_saved) # / videos_distributed


start_time = time.time()

ep_by_ep_id, size_by_video, cs_ids, cache_size, eps_by_cs = read_file(INPUT_FILE)
video_problem = VideoProblem(ep_by_ep_id, size_by_video, cs_ids, cache_size, eps_by_cs, max_iter=100000)
try:
    video_problem.run()
except KeyboardInterrupt:
    pass
finally:
    if len(video_problem.solutions.keys()) == 0:
        print 'NO SOLUTIONS FOUND'
    else:
        for ts, s in sorted(video_problem.solutions.items()):
            print ts, s
        time_saved, sol = sorted(video_problem.solutions.items())[0]
        print 'Solution', sol, time_saved
        write_solution_to_file(sol)
print
print 'Took {} second'.format(time.time() - start_time)
