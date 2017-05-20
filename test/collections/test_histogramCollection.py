from __future__ import print_function
from nose.tools import assert_equal
import cmsl1t.collections.hist as hist
from cmsl1t.geometry import is_in_region, eta_regions
from functools import partial


pileup = hist.DimensionSorted([0, 10, 15, 20, 30, 999])
dummy_factory = lambda: print("making histogram")


def test_dimension_sorted():
    assert_equal(pileup[-19],[hist.DimensionBase.underflow])
    assert_equal(pileup[9],[0])
    assert_equal(pileup[19],[2])
    assert_equal(pileup[39],[4])
    assert_equal(pileup[9999],[hist.DimensionBase.overflow])


def test_flatten_bin_list():
    bin_list = [ [1] ]
    flat_list = hist.HistogramCollection._flatten_bins(bin_list)
    assert_equal(flat_list, [ (1,) ] )


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


def test_region_binning():
    coll = hist.HistogramCollection(dimensions=1)
    coll.register_dim(1, segmentation_func=partial(
        hist.bin_finder_region, bins=regions), bins=regions)
    coll[0] = 2
    coll[2.1] = 42
    coll[5] = 234
    assert_equal(coll[-1.0], 2)
    assert_equal(coll[2.99], 42)
    assert_equal(coll[-999], 5)


def test_collection_size_1D():
    coll = hist.HistogramCollection(dimensions=1)
    coll.register_dim(1, segmentation_func=partial(
        hist.bin_finder_region, bins=regions), bins=regions)
    coll.add('histName', bins=[0, 10, 20, 30])
    assert_equal(len(coll), len(regions))


def test_collection_size_2D():
    coll = hist.HistogramCollection(dimensions=1)
    coll.register_dim(1, segmentation_func=partial(
        hist.bin_finder_sorted, bins=pileupBins), bins=pileupBins)
    coll.register_dim(2, segmentation_func=partial(
        hist.bin_finder_region, bins=regions), bins=regions)
    coll.add('histName', bins=[0, 10, 20, 30])
    assert_equal(len(coll), len(regions) * len(pileupBins))
