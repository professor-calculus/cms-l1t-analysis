import unittest
from cmsl1t.utils.timers import timerfunc


@timerfunc
def test_wrapping_method():
    pass


class TestTimerfunc(unittest.TestCase):

    def test_wrapping(self):
        wrapped = getattr(test_wrapping_method, "__wrapped__")
        self.assertEqual(wrapped.__name__, 'test_wrapping_method')
