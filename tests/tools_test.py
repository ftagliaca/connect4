from __future__ import annotations

import unittest

import numpy as np

import tools as tl


class TestCheckConseqNums(unittest.TestCase):

    def check_correct_output(self):
        arr1 = np.arange(10)
        arr2 = np.array([1, 1, 1, 3, 4, 5])
        arr3 = np.array([1, 1, 1, 1, 1, 1])

        self.assertFalse(tl.check_conseq_nums(arr1, 3))
        self.assertTrue(tl.check_conseq_nums(arr2, 3))
        self.assertTrue(tl.check_conseq_nums(arr3, 6))
