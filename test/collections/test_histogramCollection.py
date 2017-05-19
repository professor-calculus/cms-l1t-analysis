from nose.tools import assert_equal
import cmsl1t.collections.hist as hist
from cmsl1t.geometry import is_in_region, eta_regions
from functools import partial


pileupBins = [0, 10, 15, 20, 30, 999]
regions = eta_regions.keys()


def test_pileup_binning():
    coll = hist.HistogramCollection(dimensions=1)
    coll.register_dim(1, segmentation_func=partial(
        hist.bin_finder_sorted, bins=pileupBins), bins=pileupBins)
    coll[11] = 2
    coll[42] = 42
    assert_equal(coll[13], 2)
    assert_equal(coll[9999], 42)


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
