from __future__ import division
import numpy as np
from cmsl1t.plotting.base import BasePlotter
from cmsl1t.hist.hist_collection import HistogramCollection
from cmsl1t.hist.factory import HistFactory
import cmsl1t.hist.binning as bn
from cmsl1t.utils.draw import draw, label_canvas
from cmsl1t.recalc.resolution import get_resolution_function
from cmsl1t.utils.hist import cumulative_hist, normalise_to_collision_rate
from cmsl1t.utils.hist import normalise_to_unit_area


from rootpy.context import preserve_current_style
from rootpy.plotting import Legend


class RatesPlot(BasePlotter):

    def __init__(self, online_name):
        name = ["rates", online_name]
        super(RatesPlot, self).__init__("__".join(name))
        self.online_name = online_name

    def create_histograms(self,
                          online_title,
                          pileup_bins, n_bins, low, high):
        """ This is not in an init function so that we can by-pass this in the
        case where we reload things from disk """
        self.online_title = online_title
        self.pileup_bins = bn.Sorted(pileup_bins, "pileup",
                                     use_everything_bin=True)

        name = ["resolution", self.online_name, "pu_{pileup}"]
        name = "__".join(name)
        title = " ".join([self.online_name, "vs.", "in PU bin: {pileup}"])
        title = ";".join([title, self.online_title])
        self.plots = HistogramCollection([self.pileup_bins],
                                         "Hist1D", n_bins, low, high,
                                         name=name, title=title)
        self.filename_format = name

    def fill(self, pileup, online):
        self.plots[pileup].fill(online)

    def draw(self, with_fits=False):
        hists = []
        labels = []
        fits = []
        for (pile_up, ), hist in self.plots.flat_items_all():
            h = cumulative_hist(hist)
            h = normalise_to_collision_rate(h)
            if pile_up == bn.Base.everything:
                h.linestyle = "dashed"
                label = "Everything"
            elif isinstance(pile_up, int):
                h.drawstyle = "EP"
                label = "~ {:.0f}".format(
                    self.pileup_bins.get_bin_center(pile_up))
            else:
                continue
            h.SetMarkerSize(0.5)
            hists.append(h)
            labels.append(label)
            # if with_fits:
            #     fits.append(self.fits.get_bin_contents([pile_up]))
        self.__make_overlay(hists, fits, labels, "Number of events")

        normed_hists = list(normalise_to_unit_area(hists))
        self.__make_overlay(normed_hists, fits, labels,
                            "Fraction of events", "__shapes")

    def overlay_with_emu(self, emu_plotter, with_fits=False):
        hists = []
        labels = []
        fits = []
        for (pile_up, ), hist in self.plots.flat_items_all():
            h = cumulative_hist(hist)
            bin1 = h.get_bin_content(1)
            if pile_up == bn.Base.everything:
                h.SetLineStyle(1)
                h.drawstyle = "hist"
                label = "HW, all PU"
            else:
                continue
            h.SetLineWidth(5)
            h.SetMinimum(0.1)
            hists.append(h)
            labels.append(label)

        for (pile_up, ), hist in emu_plotter.plots.flat_items_all():
            h = get_cumulative_unscaled_hist(hist)
            bin1 = h.get_bin_content(1)
            if pile_up == bn.Base.everything:
                h.SetLineStyle(7)
                h.drawstyle = "hist"
                label = "Emu, all PU"
            else:
                continue
            h.SetLineWidth(5)
            h.SetMinimum(0.1)
            hists.append(h)
            labels.append(label)

        self.__make_overlay(hists, fits, labels, "Number of events", "__Overlay_Emu", legendtitle="", setlogy=True)

        normed_hists = [hist / hist.integral() if hist.integral() != 0 else hist.Clone() for hist in hists]
        self.__make_overlay(normed_hists, fits, labels, "Fraction of events", "__shapes__Overlay_Emu", legendtitle="")

    def __make_overlay(self, hists, fits, labels, ytitle, suffix="", legendtitle="Pile-up bin", setlogy=False):
        with preserve_current_style():
            # Draw each resolution (with fit)
            xtitle = self.online_title
            canvas = draw(hists, draw_args={
                          "xtitle": xtitle, "ytitle": ytitle, "logy": setlogy})
            if fits:
                for fit, hist in zip(fits, hists):
                    fit["asymmetric"].linecolor = hist.GetLineColor()
                    fit["asymmetric"].Draw("same")

            # Add labels
            label_canvas()

            # Add a legend
            legend = Legend(len(hists), header=legendtitle,
                            topmargin=0.35, entryheight=0.035)
            for hist, label in zip(hists, labels):
                legend.AddEntry(hist, label)
            legend.SetBorderSize(0)
            legend.Draw()

            # Save canvas to file
            name = self.filename_format.format(pileup="all")
            self.save_canvas(canvas, name + suffix)

    def _is_consistent(self, new):
        """
        Check the two plotters are the consistent, so same binning and same axis names
        """
        return all([self.pileup_bins.bins == new.pileup_bins.bins,
                    self.online_name == new.online_name,
                    ])

    def _merge(self, other):
        """
        Merge another plotter into this one
        """
        self.plots += other.plots
        return self.plots
