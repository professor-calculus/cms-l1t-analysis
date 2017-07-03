from __future__ import print_function
from cmsl1t.hist.hist_collection import HistogramCollection
from cmsl1t.hist.factory import HistFactory
import cmsl1t.hist.binning as bn
from cmsl1t.utils.draw import draw, label_canvas
from cmsl1t.utils.fit_efficiency import fit_efficiency
from cmsl1t.io import to_root

from rootpy.plotting import Legend, HistStack
from rootpy.context import preserve_current_style


class EfficiencyPlot():
    def build(self,
              online_name, offline_name,
              online_title, offline_title,
              pileup_bins, thresholds, n_bins, low, high):
        """ This is not in an init function so that we can by-pass this in the
        case where we reload things from disk """
        self.online_name = online_name
        self.offline_name = offline_name
        self.online_title = online_title
        self.offline_title = offline_title
        self.pileup_bins = bn.Sorted(pileup_bins, "pileup",
                                     use_everything_bin=True)
        self.thresholds = bn.GreaterThan(thresholds, "threshold",
                                         use_everything_bin=True)

        name = [online_name, offline_name,
                "thresh_{threshold}", "pu_{pileup}"]
        name = "__".join(name)
        title = " ".join([online_name, " in PU bin: {pileup}",
                          "and passing threshold: {threshold}"])
        self.yields = HistogramCollection([self.pileup_bins, self.thresholds],
                                          "Hist1D", n_bins, low, high,
                                          name="yield" + name, title=title)
        self.filename_format = "{outdir}/{type}" + name + ".{fmt}"

    def set_plot_output_cfg(self, outdir, fmt):
        self.output_dir = outdir
        self.output_format = fmt

    def from_root(self, filename):
        """ Reload histograms from existing files on disk """
        pass

    def to_root(self, filename):
        """ Write histograms to disk """
        to_write = [self, self.yields]
        if hasattr(self, "efficiencies"):
            to_write += [self.efficiencies]
        to_root(to_write, filename)

    def fill(self, pileup, online, offline):
        self.yields[pileup, online].fill(offline)

    def draw(self, with_fits=True):
        # Calclate the efficiency for each threshold
        self.__fill_efficiencies()
        if with_fits:
            self.__fit_efficiencies()

        # Overlay the "all" pile-up bin for each threshold
        all_pileup_effs = self.efficiencies.get_bin_contents([bn.Base.everything])
        hists = []
        labels = []
        fits = []
        for threshold in all_pileup_effs.iter_all():
            if not isinstance(threshold, int):
                continue
            hists.append(all_pileup_effs.get_bin_contents(threshold))
            labels.append("> " + str(self.thresholds.bins[threshold]))
            if with_fits:
                fits.append(self.fits.get_bin_contents([bn.Base.everything, threshold]))
        self.__make_overlay("all", "all", hists, fits, labels, self.online_title)

        # Overlay individual pile-up bins for each threshold
        for threshold in self.thresholds:
            hists = []
            labels = []
            fits = []
            for pileup in self.pileup_bins.iter_all():
                if not isinstance(pileup, int):
                    continue
                hists.append(self.efficiencies.get_bin_contents([pileup, threshold]))
                if with_fits:
                    fits.append(self.fits.get_bin_contents([pileup, threshold]))
                labels.append(str(self.pileup_bins.bins[pileup]))
            self.__make_overlay(pileup, threshold, hists, fits, labels, "PU bin")

        # Produce the fit summary plot
        if with_fits:
            self.__summarize_fits()

    def __fill_efficiencies(self):
        # Boiler plate to convert a given distribution to a efficiency
        def make_eff(labels):
            pileup_bin = labels["pileup"]
            threshold_bin = labels["threshold"]
            total = self.yields.get_bin_contents([pileup_bin, bn.Base.everything])
            passed = self.yields.get_bin_contents([pileup_bin, threshold_bin])
            efficiency = passed.Clone(passed.name.replace("yield", "efficiency"))
            efficiency.Divide(total)
            return efficiency

        # Actually make the efficiencies
        self.efficiencies = HistogramCollection([self.pileup_bins, self.thresholds],
                                                make_eff)

    def __fit_efficiencies(self):
        def make_fit(labels):
            pileup_bin = labels["pileup"]
            threshold_bin = labels["threshold"]
            efficiency = self.efficiencies.get_bin_contents([pileup_bin, threshold_bin])
            params = fit_efficiency(efficiency, self.thresholds.get_bin_center(threshold_bin))
            return params

        # Actually make the efficiencies
        self.fits = HistogramCollection([self.pileup_bins, self.thresholds],
                                        make_fit)

    def __make_overlay(self, pileup, threshold, hists, fits, labels, header):
        with preserve_current_style():
            # Draw each efficiency (with fit)
            canvas = draw(hists, draw_args={"xtitle": self.offline_title,
                                            "ytitle": "Efficiency"})
            if len(fits) > 0:
                for fit, hist in zip(fits, hists):
                    fit["asymmetric"].linecolor = hist.GetLineColor()
                    fit["asymmetric"].Draw("same")

            # Add labels
            label_canvas()

            # Add a legend
            legend = Legend(len(hists), header=header)
            for hist, label in zip(hists, labels):
                legend.AddEntry(hist, label)
            legend.Draw()

            # Save canvas to file
            filename = self.filename_format
            filename = filename.format(type="efficiency_",
                                       outdir=self.output_dir,
                                       pileup=pileup,
                                       threshold=threshold,
                                       fmt="png")
            canvas.SaveAs(filename)

    def __summarize_fits(self):
        pass
