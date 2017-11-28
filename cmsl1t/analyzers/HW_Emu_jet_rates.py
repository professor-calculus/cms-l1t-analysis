"""
Study the MET distibutions and various PUS schemes
"""
import numpy as np
import six
import ROOT
import os
from cmsl1t.analyzers.BaseAnalyzer import BaseAnalyzer
from cmsl1t.collections import HistogramsByPileUpCollection
from cmsl1t.utils.draw import draw, label_canvas
from cmsl1t.plotting.rates import RatesPlot
import cmsl1t.hist.binning as bn


sum_types = [
    "HTT", "MHT", "MET_HF", "MET", "MET_PF", "MET_PF_NoMu", "MET_PF_HF",
    "MET_PF_NoMu_HF",
]

jet_types = ["singlel1JetEt", "doublel1JetEt", "triplel1JetEt", "quadl1JetEt"]

HW_types = sum_types + jet_types

sum_types += [t + '_Emu' for t in sum_types]
jet_types += [u + '_Emu' for u in jet_types]

object_types = sum_types + jet_types

def ExtractSums(event):
    online = dict(
        HTT=event.l1Sums["L1Htt"],
        MHT=event.l1Sums["L1Mht"],
        MET_HF=event.l1Sums["L1MetHF"],
        MET=event.l1Sums["L1Met"],
        MET_PF=event.l1Sums["L1Met"],
        MET_PF_NoMu=event.l1Sums["L1Met"],
        MET_PF_HF=event.l1Sums["L1MetHF"],
        MET_PF_NoMu_HF=event.l1Sums["L1MetHF"],
        HTT_Emu=event.l1Sums["L1EmuHtt"],
        MHT_Emu=event.l1Sums["L1EmuMht"],
        MET_HF_Emu=event.l1Sums["L1EmuMetHF"],
        MET_Emu=event.l1Sums["L1EmuMet"],
        MET_PF_Emu=event.l1Sums["L1EmuMet"],
        MET_PF_NoMu_Emu=event.l1Sums["L1EmuMet"],
        MET_PF_HF_Emu=event.l1Sums["L1EmuMetHF"],
        MET_PF_NoMu_HF_Emu=event.l1Sums["L1EmuMetHF"]
    )
    return online

class Analyzer(BaseAnalyzer):

    def __init__(self, config, **kwargs):
        super(Analyzer, self).__init__("HW_Emu_jet_rates", config)
        self.triggerName = self.config.get('input', 'trigger')['name']

        for name in object_types:
            rates_plot = RatesPlot(name)
            self.register_plotter(rates_plot)
            setattr(self, name + "_rates", rates_plot)

    def prepare_for_events(self, reader):
        bins = np.arange(0.0, 400.0, 1.0)
        puBins = self.puBins

        for name in object_types:
            rates_plot = getattr(self, name + "_rates")
            rates_plot.build(name, puBins, 400, 0, 400)

        '''
        self.rates = HistogramsByPileUpCollection(
            pileupBins=puBins, dimensions=2)
        for thing in object_types:
            self.rates.add(thing, bins)
        '''

        return True
    
    '''
    def reload_histograms(self, input_file):
        # Something like this needs to be implemented still
        self.rates = HistogramsByPileUpCollection.from_root(input_file)
        return True
    '''

    def fill_histograms(self, entry, event):
        
        # Get pileup if ntuples have reco trees in them.
        # If not, set PU to 1 so that it fills the (only) pu bin.

        try:
            pileup = event.nVertex
        except AttributeError:
            pileup = 1.

        #Sums:
        online = ExtractSums(event)
        for name in sum_types:
            on = online[name]
            getattr(self, name + "_rates").fill(pileup, on.et)

        #Jets:
        l1JetEts = [jet.et for jet in event._l1Jets]
        nJets = len(l1JetEts)
        if nJets > 0:
            maxL1JetEt = max(l1JetEts)
        else:
            maxL1JetEt = 0.


        l1EmuJetEts = [jet.et for jet in event._l1EmuJets]
        nEmuJets = len(l1EmuJetEts)
        if nEmuJets > 0:
            maxL1EmuJetEt = max(l1EmuJetEts)
        else:
            maxL1EmuJetEt = 0.


        if nJets == 0:
            getattr(self, 'singlel1JetEt_rates').fill(pileup, 0.)
            getattr(self, 'doublel1JetEt_rates').fill(pileup, 0.)
            getattr(self, 'triplel1JetEt_rates').fill(pileup, 0.)
            getattr(self, 'quadl1JetEt_rates').fill(pileup, 0.)
        if nJets >= 1:
            getattr(self, 'singlel1JetEt_rates').fill(pileup, maxL1JetEt)
        if nJets >= 2:
            getattr(self, 'doublel1JetEt_rates').fill(pileup, maxL1JetEt)
        if nJets >= 3:
            getattr(self, 'triplel1JetEt_rates').fill(pileup, maxL1JetEt)
        if nJets >= 4:
            getattr(self, 'quadl1JetEt_rates').fill(pileup, maxL1JetEt)

        if nEmuJets == 0:
            getattr(self, 'singlel1JetEt_Emu_rates').fill(pileup, 0.)
            getattr(self, 'doublel1JetEt_Emu_rates').fill(pileup, 0.)
            getattr(self, 'triplel1JetEt_Emu_rates').fill(pileup, 0.)
            getattr(self, 'quadl1JetEt_Emu_rates').fill(pileup, 0.)
        if nEmuJets >= 1:
            getattr(self, 'singlel1JetEt_Emu_rates').fill(pileup, maxL1EmuJetEt)
        if nEmuJets >= 2:
            getattr(self, 'doublel1JetEt_Emu_rates').fill(pileup, maxL1EmuJetEt)
        if nEmuJets >= 3:
            getattr(self, 'triplel1JetEt_Emu_rates').fill(pileup, maxL1EmuJetEt)
        if nEmuJets >= 4:
            getattr(self, 'quadl1JetEt_Emu_rates').fill(pileup, maxL1EmuJetEt)

        return True

    def make_plots(self):
        # TODO: implement this in BaseAnalyzer
        # make_plots -> make_plots(plot_func)

        # Get EMU thresholds for each HW threshold.

        THRESHOLDS = self.thresholds
        if THRESHOLDS == None:
            print('Error: Please specify thresholds in the config .yaml in dictionary format')

        for i in ['HF', 'PF', 'PF_NoMu', 'PF_HF', 'PF_NoMu_HF']:
            if THRESHOLDS['MET_' + i] == None:
                THRESHOLDS['MET_' + i] = THRESHOLDS['MET']

        for j in ['doublel1JetEt', 'triplel1JetEt', 'quadl1JetEt']:
            if THRESHOLDS[j] == None:
                THRESHOLDS[j] = THRESHOLDS['singlel1JetEt']

        # calculate cumulative histograms
        for plot in self.all_plots:
            hist = plot.plots.get_bin_contents([bn.Base.everything])
            bin1 = hist.get_bin_content(1)
            if bin1 != 0.:
                hist.Scale(40000000./bin1)
            h = get_cumulative_hist(hist)
            bin1cumul = h.get_bin_content(1)
            if bin1cumul != 0.:
                h.Scale(40000000./bin1cumul)
            setattr(self, plot.online_name, h)
            plot.draw()

        print('  thresholds:')

        for histo_name in HW_types:
            h = getattr(self, histo_name)
            h_emu = getattr(self, histo_name + "_Emu")
            bin1 = h.get_bin_content(1)
            if bin1 != 0.:
                h.Scale(40000000./bin1)
            bin1_emu = h_emu.get_bin_content(1)
            if bin1_emu != 0.:
                h_emu.Scale(40000000./bin1_emu)
            thresholds = THRESHOLDS.get(histo_name)
            emu_thresholds = []
            for thresh in thresholds:
                rate_delta = []
                hw_rate = h.get_bin_content(thresh)
                for i in range(h.nbins()):
                    emu_rate = h_emu.get_bin_content(i)
                    if hw_rate == 0. or emu_rate == 0.:
                        rate_delta.append(40000000.)
                    else:
                        rate_delta.append(abs(hw_rate - emu_rate))
                emu_thresholds.append(rate_delta.index(min(rate_delta)))
            outputline = ('    {0}: {1}'.format(histo_name, thresholds) + '\n'
                          + '    {0}: {1}'.format(histo_name + '_Emu', emu_thresholds))
            print(outputline)

        '''
        for histo_name in object_types:
            h = getattr(self, histo_name)
            plot(h, histo_name, self.output_folder)
        '''
        return True


def _reverse(a):
    return np.array(np.flipud(a))


def get_cumulative_hist(hist):
    h = hist.clone(hist.name + '_cumul')
    arr = np.cumsum(_reverse([bin.value for bin in hist]))
    h.set_content(_reverse(arr))
    errors_sq = np.cumsum(_reverse([bin.error**2 for bin in hist]))
    h.set_error(_reverse(np.sqrt(errors_sq)))

    # now scale
    bin1 = h.get_bin_content(1)
    if bin1 != 0:
        h.GetSumw2()
        h.Scale(4.0e7 / bin1)
    return h


def plot(hist, name, output_folder):
    pu = ''
    if '_pu' in name:
        pu = name.split('_')[-1]
        name = name.replace('_' + pu, '')
    file_name = 'rates_{name}'.format(name=name)
    if 'nVertex' in name:
        file_name = 'nVertex'
    if pu:
        file_name += '_' + pu
    canvas_name = file_name.replace('SingleMu', 'Rates')
    c = ROOT.TCanvas(canvas_name)
    if 'nVertex' not in name:
        c.SetLogy()
    hist.set_y_title('Rate (Hz)')
    hist.set_x_title(name)
    hist.Draw()
    c.SaveAs(os.path.join(output_folder, file_name + '.pdf'))
