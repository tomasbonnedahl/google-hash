import unittest

import numpy as np

from utils import slice_within_ingredient_interval


class PractiseTest(unittest.TestCase):
    def test_within_ingredient_interval_one_each(self):
        slice = np.ones((2, 1), dtype=int)
        slice[0][0] = 2

        assert slice_within_ingredient_interval(slice, min_ing_per_slice=1)

    def test_within_ingredient_interval_both_M(self):
        slice = np.ones((2, 1), dtype=int)
        assert not slice_within_ingredient_interval(slice, min_ing_per_slice=1)

    def test_within_ingredient_interval_both_T(self):
        slice = np.ones((2, 1), dtype=int)
        slice[0][0] = 2
        slice[1][0] = 2

        assert not slice_within_ingredient_interval(slice, min_ing_per_slice=1)

    def test_within_ingredient_interval_both_T_horz(self):
        slice = np.ones((1, 2), dtype=int)
        slice[0][0] = 2
        slice[0][1] = 2

        assert not slice_within_ingredient_interval(slice, min_ing_per_slice=1)

    def test_within_ingredient_interval_one_each_2_2(self):
        slice = np.ones((2, 2), dtype=int)
        slice[0][0] = 2
        slice[1][0] = 2

        assert slice_within_ingredient_interval(slice, min_ing_per_slice=2)

    def test_within_ingredient_interval_one_each_2_2_M(self):
        slice = np.ones((2, 2), dtype=int)
        slice[0][0] = 2

        assert not slice_within_ingredient_interval(slice, min_ing_per_slice=2)

    def test_within_ingredient_interval_one_each_2_2_T(self):
        slice = np.ones((2, 2), dtype=int)
        slice[0][0] = 2
        slice[1][0] = 2
        slice[0][1] = 2

        assert not slice_within_ingredient_interval(slice, min_ing_per_slice=2)

    def test_within_ingredient_interval_one_each_2_2_only_M(self):
        slice = np.ones((2, 2), dtype=int)
        assert not slice_within_ingredient_interval(slice, min_ing_per_slice=2)

    def test_within_ingredient_interval_one_each_2_2_only_T(self):
        slice = np.ones((2, 2), dtype=int)
        slice[0][0] = 2
        slice[1][0] = 2
        slice[0][1] = 2
        slice[1][1] = 2

        assert not slice_within_ingredient_interval(slice, min_ing_per_slice=2)

    def test_within_ingredient_interval_one_each_3_3(self):
        slice = np.ones((3, 3), dtype=int)
        slice[0][0] = 2
        slice[1][0] = 2
        slice[0][1] = 2
        slice[1][1] = 2

        assert slice_within_ingredient_interval(slice, min_ing_per_slice=4)

    def test_within_ingredient_interval_one_each_3_3_M(self):
        slice = np.ones((3, 3), dtype=int)
        slice[0][0] = 2
        slice[1][0] = 2
        slice[1][1] = 2

        assert not slice_within_ingredient_interval(slice, min_ing_per_slice=4)

    def test_within_ingredient_interval_one_each_3_3_T(self):
        slice = np.ones((3, 3), dtype=int)
        slice[0][0] = 2
        slice[1][0] = 2
        slice[0][1] = 2
        slice[1][1] = 2
        slice[2][1] = 2
        slice[2][2] = 2

        assert not slice_within_ingredient_interval(slice, min_ing_per_slice=4)
