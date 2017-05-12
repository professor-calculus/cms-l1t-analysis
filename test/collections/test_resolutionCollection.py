from cmsl1t.collections import ResolutionCollection
import cmsl1t.geometry as geo
import unittest


class TestResolutionCollection(unittest.TestCase):

    def test_add_variable(self):
        pileupBins = [0, 10, 15, 20, 30, 999]
        hists = ResolutionCollection(
            pileupBins=pileupBins, regions=geo.eta_regions)
        # this should create 1 entry for every pileup bin and every region
        hists.add_variable('jetEt', [0, 30, 50, 100])
        expected_len = (len(pileupBins) - 1) * len(geo.eta_regions)
        self.assertEqual(len(hists), expected_len)
