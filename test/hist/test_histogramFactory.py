from __future__ import print_function
from collections import defaultdict
from nose.tools import assert_is_instance, assert_true
from rootpy.plotting.hist import Hist1D, Hist2D
from cmsl1t.hist import BaseHistogram
from cmsl1t.hist.factory import build_hist


class DummyHist(BaseHistogram):

    def __init__(self, name, title):
        super(DummyHist, self).__init__(name, title)
        self.bins = defaultdict(int)

    def fill(self, value, weight=1):
        self.bins[int(value)] += weight


def test_build_rootpy_hist():
    hist = build_hist("Hist1D", 10, 0, 1,
                      name="test_Hist1D", title="This is just another test")
    assert_true(hist.InheritsFrom(Hist1D.Class()))

    hist = build_hist("Hist2D", 10, 0, 1, 10, 2, 5,
                      name="test_Hist2D", title="This is just a test")
    assert_true(hist.InheritsFrom(Hist2D.Class()))


def test_build_custom_hist():
    hist = build_hist("DummyHist",
                      name="test_DummyHist",
                      title="This is just yet another test")
    assert_is_instance(hist, DummyHist)
