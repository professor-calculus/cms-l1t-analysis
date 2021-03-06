"""
Study the MET distibutions and various PUS schemes
"""

from BaseAnalyzer import BaseAnalyzer
from cmsl1t.collections import ResolutionCollection
import math
import ROOT
import os
from cmsl1t.filters import muonfilter


class Analyzer(BaseAnalyzer):

    def __init__(self, config, **kwargs):
        super(Analyzer, self).__init__("jet_resolution_analyzer", config)
        self.triggerName = self.config.get('input', 'trigger')['name']

    def prepare_for_events(self, reader):
        # bins = np.arange(0, 200, 25)
        # thresholds = [70, 90, 110]
        puBins = range(0, 50, 10) + [999]

        self.resolutions = ResolutionCollection(pileupBins=puBins)
        self.resolutions.add_variable('JetEt', vtype='energy')
        self.resolutions.add_variable('JetEta', vtype='position')
        self.resolutions.add_variable('JetPhi', vtype='position')

        return True

    def reload_histograms(self, input_file):
        # Something like this needs to be implemented still
        # self.resolutions = ResolutionCollection.from_root(input_file)
        return True

    def fill_histograms(self, entry, event):
        if self.triggerName == 'SingleMu':
            if not muonfilter(event.muons):
                return True
        pileup = event.nVertex

        leadingRecoJet = event.getLeadingRecoJet()
        matchedL1Jet = event.getMatchedL1Jet(leadingRecoJet)

        if not leadingRecoJet or not matchedL1Jet:
            return True

        recoEt = leadingRecoJet.etCorr
        recoEta = leadingRecoJet.eta
        recoPhi = foldPhi(leadingRecoJet.phi)

        l1Et = matchedL1Jet.et
        l1Eta = matchedL1Jet.eta
        l1Phi = foldPhi(matchedL1Jet.phi)

        resolution_et = (l1Et - recoEt) / recoEt if recoEt != 0 else 0

        resolution_eta = l1Eta - recoEta
        # should it not be
        # resolution_eta = abs(l1Et - recoEta)
        # ?
        resolution_phi = l1Phi - recoPhi
        self.resolutions.set_pileup(pileup)
        self.resolutions.set_region_by_eta(recoEta)
        self.resolutions.fill('JetEt', resolution_et)
        self.resolutions.fill('JetEta', resolution_eta)
        self.resolutions.fill('JetPhi', resolution_phi)

        return True

    def write_histograms(self):
        self.resolutions.to_root(self.get_histogram_filename())
        return True

    def make_plots(self):
        from rootpy.io import root_open
        with root_open(self.get_histogram_filename()) as f:
            # our collections are flat, need only the objects
            for _, _, objects in f.walk():
                for name in objects:
                    if 'pickle' in name:
                        continue
                    obj = f.get(name)
                    plot(obj, name, self.output_folder)
        return True


def plot(hist, name, output_folder):
    pu = ''
    if '_pu' in name:
        pu = name.split('_')[-1]
        name = name.replace('_' + pu, '')
    file_name = 'res_SingleMu_reco{name}_l1{name}'.format(name=name)
    if 'nVertex' in name:
        file_name = 'nVertex'
    if pu:
        file_name += '_' + pu
    canvas_name = file_name.replace('SingleMu', 'Energy')
    if 'JetEta' in name or 'JetPhi' in name:
        canvas_name.replace('Energy', 'Position')
    c = ROOT.TCanvas(canvas_name)
    hist.Draw()
    c.SaveAs(os.path.join(output_folder, file_name + '.pdf'))


def foldPhi(phi):
    return min([abs(phi), abs(2 * math.pi - phi)])
