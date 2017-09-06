from __future__ import print_function
from nose.tools import assert_equal
from cmsl1t.plotting.efficiency import EfficiencyPlot
import cmsl1t.hist.binning as bn
from rootpy.io import root_open
import numpy as np


n_points = 1000
offline_data = np.random.uniform(0, 100, n_points)
online_data = offline_data + np.random.normal(10, 10, n_points)


def test_EffiencyPlot_noPU_oneThreshold():
    on_vs_off_efficiency = EfficiencyPlot("online", "offline")
    off_vs_off_efficiency = EfficiencyPlot("offline", "offline")
    on_vs_on_efficiency = EfficiencyPlot("online", "online")

    puBins = [0, 999]
    thresholds = [25]
    on_vs_off_efficiency.build("Test online", "Test offline", puBins, thresholds, 50, 0, 300)
    off_vs_off_efficiency.build("Test offline", "Test offline", puBins, thresholds, 50, 0, 300)
    on_vs_on_efficiency.build("Test online", "Test online", puBins, thresholds, 50, 0, 300)

    plotters = [on_vs_off_efficiency, off_vs_off_efficiency, on_vs_on_efficiency]
    for plotter in plotters:
        plotter.set_plot_output_cfg("tests/outputs", "png")

    pileup = 3  # dummy pile-up, we don't really care here
    for on, off in zip(online_data, offline_data):
        on_vs_off_efficiency.fill(pileup, on, off)
        on_vs_on_efficiency.fill(pileup, on, on)
        off_vs_off_efficiency.fill(pileup, off, off)

    # with root_open("test/outputs/plotting-test_efficiency.root", "w") as out_file:
    #     for plotter in plotters:
    #         plotter.to_root(out_file.mkdir(plotter.directory_name))

    for plotter in plotters:
        above_50 = plotter.efficiencies.get_bin_contents([bn.Base.everything, 0])
        non_integral = [eff for eff in above_50 if eff != int(eff)]
        plotter.n_non_integral = len(non_integral)

    assert_equal(0, on_vs_on_efficiency.n_non_integral)
    assert_equal(0, off_vs_off_efficiency.n_non_integral)
