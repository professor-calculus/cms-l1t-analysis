from __future__ import print_function
import unittest
from cmsl1t.math import _reversed_cumulative_sum


class TestMath(unittest.TestCase):

    def test_reversed_cumulative_sum(self):
        values = [1, 2, 3, 4]
        expected = [10, 9, 7, 4]
        result = _reversed_cumulative_sum(values).tolist()
        self.assertListEqual(result, expected)
