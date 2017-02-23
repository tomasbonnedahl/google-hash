import numpy as np


def read_file(input_file_name):
    f_in = open(input_file_name, 'r')
    header = map(int, f_in.readline().rstrip().split())
    a, b, c = map(int, header)

    for row_index, line in enumerate(f_in):
        for col_index, ingredient in enumerate(line.rstrip()):
            pass

