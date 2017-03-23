from cmsl1t.collections import HistogramsByPileUpCollection
import unittest
import random


class TestHistogramsByPileupCollection(unittest.TestCase):

    def test__get_pu_bin(self):
        hists = HistogramsByPileUpCollection(
            pileupBins=[0, 10, 15, 20, 30, 999])
        bins = map(hists._get_pu_bin, [0, 5, 9, 10, 14, 16, 20, 35])
        expect = [0, 0, 0, 1, 1, 2, 3, 4, -1]
        for b, e in zip(bins, expect):
            self.assertEqual(b, e)

    def test_2dim(self):
        hists = HistogramsByPileUpCollection(
            pileupBins=[0, 10, 15, 20, 30, 999], dimensions=2)
        value = random.randint(-1000, 1000)
        hists[2]['a'] = value
        self.assertEqual(hists[0]['a'], value)

    def test_3dim(self):
        hists = HistogramsByPileUpCollection(
            pileupBins=[0, 10, 15, 20, 30, 999], dimensions=3)
        value = random.randint(-1000, 1000)
        hists[2]['a']['b'] = value
        self.assertEqual(hists[0]['a']['b'], value)
