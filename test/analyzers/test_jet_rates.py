from cmsl1t.analyzers.jet_rates import get_cumulative_hist
import numpy as np
import math
from rootpy.plotting import Hist

from nose.tools import (raises, assert_equal, assert_almost_equal,
                        assert_raises, assert_true, assert_false)

def test_cumulative_hist():
    hist = Hist(10, 0, 1)
    hist.FillRandom('gaus')
    h_loop = hist.clone('loop')
    entries = [bin_i.value for bin_i in hist]
    errors_sq = [bin_i.error**2 for bin_i in hist]
    for i, entry in enumerate(entries):
        content = sum(entries[i:])
        error = sum(errors_sq[i:])
        h_loop.set_bin_content(i, content)
        h_loop.set_bin_error(i, math.sqrt(error))

    h_loop.Scale(4.0e7/h_loop.get_bin_content(1))
    h_cumul = get_cumulative_hist(hist)

    entries_loop = [bin_i.value for bin_i in h_loop]
    entries_func = [bin_i.value for bin_i in h_cumul]
    assert_equal(entries_loop, entries_func)

    errors_loop = [bin_i.error for bin_i in h_loop]
    errors_func = [bin_i.error for bin_i in h_cumul]
    assert_equal(errors_loop, errors_func)
