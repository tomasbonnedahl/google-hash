from collections import defaultdict

import datetime


class EndPoint(object):
    def __init__(self, id):
        self.id = id
        self.requests_by_video = {}
        self.latency_by_cs = {}
        self.dc_latency = 0

    def __str__(self):
        return str(self.id) + ": " + str(self.dc_latency) + ", " + str(self.latency_by_cs.values())


def read_file(input_file_name):
    f_in = open(input_file_name, 'r')
    header = map(int, f_in.readline().rstrip().split())
    num_videos, num_endpoints, num_requests, num_caches, cache_size = header

    videos = map(int, f_in.readline().rstrip().split())
    size_by_video = {}
    for video_index, video_size in zip(xrange(100), videos):
        size_by_video[video_index] = video_size

    ep_by_ep_id = {x: EndPoint(x) for x in xrange(num_endpoints)}

    cs_ids = []

    eps_by_cs = defaultdict(list)

    for row_index, line in enumerate(f_in):
        try:
            ep_dc_latency, num_cs_for_this_ep = map(int, line.rstrip().split())
            ep_by_ep_id[row_index].dc_latency = ep_dc_latency
            for _ in xrange(num_cs_for_this_ep):
                cs_id, ep_cs_latency = map(int, f_in.next().rstrip().split())
                cs_ids.append(cs_id)
                eps_by_cs[cs_id].append(ep_by_ep_id[row_index])
                ep_by_ep_id[row_index].latency_by_cs[cs_id] = ep_cs_latency
        except ValueError:
            break

    for row_index, line in enumerate(f_in):
        video_id, ep_id, ep_requests = map(int, line.rstrip().split())
        ep_by_ep_id[ep_id].requests_by_video[video_id] = ep_requests

    return ep_by_ep_id, size_by_video, cs_ids, cache_size, eps_by_cs


def write_solution_to_file(solution):
    t = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
    output_file_name = "me_at_the_zoo-" + t + ".out"
    with open(output_file_name, 'w') as f:
        f.write('{}\n'.format(len(solution.keys())))
        write_cache_servers(f, solution)
    print
    print 'Solution written to:', output_file_name


def write_cache_servers(f, solution):
    for cs_id, videos in solution.items():
        l = [cs_id] + list(videos)
        l = map(str, l)
        row = " ".join(l)
        f.write('{}\n'.format(row))
