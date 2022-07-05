from __future__ import annotations

import unittest
from itertools import product

import numpy as np

import tools as tl


class TestCheckConseqNums(unittest.TestCase):

    def test_correct_output(self):
        arr1 = np.arange(10)
        arr2 = np.array([1, 1, 1, 3, 4, 5])
        arr3 = np.array([1, 1, 1, 1, 1, 1])

        arr1_ret = tl.check_conseq_nums(arr1, 3)
        arr2_ret = tl.check_conseq_nums(arr2, 3)
        arr3_ret = tl.check_conseq_nums(arr3, 6)
        self.assertFalse(arr1_ret[0])
        self.assertEqual(arr1_ret[1], -1)
        self.assertTrue(arr2_ret[0])
        self.assertEqual(arr2_ret[1], 1)
        self.assertTrue(arr3_ret[0])
        self.assertEqual(arr3_ret[1], 1)

    def test_output_for_game(self):

        for arr in map(np.array, product(range(3), repeat=7)):
            center_number = arr[3]
            win1 = np.all(arr[:4] == center_number)
            win2 = np.all(arr[1:5] == center_number)
            win3 = np.all(arr[2:6] == center_number)
            win4 = np.all(arr[3:7] == center_number)
            win = win1 or win2 or win3 or win4
            ret = tl.check_conseq_nums(arr, 4)
            self.assertEqual(ret[0], win)
            self.assertEqual(ret[1], center_number if win else -1)
