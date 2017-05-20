from __future__ import print_function
from nose.tools import assert_equal
import cmsl1t.collections.hist as hist
from cmsl1t.geometry import is_in_region, eta_regions
from functools import partial


pileup = hist.DimensionSorted([0, 10, 15, 20, 30, 999])
multi = hist.DimensionOverlappingBins([(0,10),(100,110),(5,15)])
regions = hist.DimensionRegion()
dummy_factory = lambda: print("making histogram")


def test_dimension_sorted():
    assert_equal(pileup[-19],[hist.DimensionBase.underflow])
    assert_equal(pileup[9],[0])
    assert_equal(pileup[19],[2])
    assert_equal(pileup[39],[4])
    assert_equal(pileup[9999],[hist.DimensionBase.overflow])


def test_dimension_multi():
    assert_equal(multi[3],[0])
    assert_equal(multi[7],[0,2])
    assert_equal(multi[105],[1])
    assert_equal(multi[70],[hist.DimensionBase.overflow])


def test_dimension_region():
    assert_equal(regions[0],["BE", "B"])
    assert_equal(regions[2],["BE", "E"])
    assert_equal(regions[3.1],["HF"])


def test_flatten_bin_list():
    bin_list = [ [1] ]
    flat_list = hist.HistogramCollection._flatten_bins(bin_list)
    assert_equal(flat_list, [ (1,) ] )
    bin_list = [ [1],[2,3] ]
    flat_list = hist.HistogramCollection._flatten_bins(bin_list)
    assert_equal(flat_list, [ (1,2),(1,3) ] )


def test_find_bins():
    coll = hist.HistogramCollection(
            dimensions=[pileup],
            histogram_factory=dummy_factory
            )
    coll[11] = 2
    coll[42] = 42
    assert_equal(coll._find_bins(-20), [ (hist.DimensionBase.underflow,)] )
    assert_equal(coll._find_bins(13), [ (1,)] )
    assert_equal(coll._find_bins(47), [ (4,)] )
    assert_equal(coll._find_bins(9999), [ (hist.DimensionBase.overflow,)] )


def test_pileup_binning():
    coll = hist.HistogramCollection(
            dimensions=[pileup],
            histogram_factory=dummy_factory
            )
    coll[-3] = 6
    coll[11] = 2
    coll[42] = 42
    coll[10044] = 49
    assert_equal(coll[-20], 6)
    assert_equal(coll[13], 2 )
    assert_equal(coll[47], 42 )
    assert_equal(coll[9999], 49 )


def test_collection_2D():
    coll = hist.HistogramCollection(
            dimensions=[pileup,multi],
            histogram_factory=dummy_factory
            )
    coll[-3,4] = 6
    coll[11,105] = 49
    assert_equal(coll[-20,2], 6)
    assert_equal(coll[13,108], 49 )
