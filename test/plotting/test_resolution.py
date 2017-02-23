from cmsl1t.plotting.resolution import Resolution
import cmsl1t.geometry as geo
import unittest


class TestResolution(unittest.TestCase):

    def test_add_hist_set(self):
        r = Resolution()
        r.add_hist_set('jetEta')
        self.assertEqual(len(r._hists), len(geo.regions))
