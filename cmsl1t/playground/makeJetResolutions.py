from __future__ import print_function
import ROOT
import os
import glob
import math
import logging
from eventreader import EventReader
from cmsl1t.collections import ResolutionCollection

logging.getLogger("rootpy.tree.chain").setLevel(logging.WARNING)


FILES = glob.glob('data/*.root')


def main(n_events, output_folder):
    ROOT.PyConfig.IgnoreCommandLineOptions = True
    ROOT.gROOT.SetBatch(1)
    ROOT.TH1.SetDefaultSumw2(True)
    ROOT.gStyle.SetOptStat(0)
    histograms = ResolutionCollection(pileupBins=[0, 13, 20, 999])
    histograms.add_variable('JetEt', vtype='energy')
    histograms.add_variable('JetEta', vtype='position')
    histograms.add_variable('JetPhi', vtype='position')

    reader = EventReader(FILES, events=n_events)

    for entry, event in enumerate(reader):
        pileup = event.nVertex

        leadingRecoJet = event.getLeadingRecoJet()
        matchedL1Jet = event.getMatchedL1Jet(leadingRecoJet)

        if not leadingRecoJet:
            continue
        if not matchedL1Jet:
            continue

        # pu = event.nVertex

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
        histograms.set_pileup(pileup)
        histograms.set_region_by_eta(recoEta)
        histograms.fill('JetEt', resolution_et)
        histograms.fill('JetEta', resolution_eta)
        histograms.fill('JetPhi', resolution_phi)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, 'jetResolutions.root')
    histograms.to_root(output_file)

    # plotting should be separate, this is just here as an example
    from rootpy.io import root_open
    with root_open(output_file) as f:
        # our collections are flat, need only the objects
        for _, _, objects in f.walk():
            for name in objects:
                if 'pickle' in name:
                    continue
                obj = f.get(name)
                plot(obj, name, output_folder)
    print('Processed', entry + 1, 'events')


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


if __name__ == "__main__":
    from datetime import datetime
    TODAY = datetime.now().timetuple()
    ROOT.gSystem.Load('build/L1TAnalysisDataformats.so')
    output_folder = os.path.join(
        'benchmark', 'new',
        '{y}{m:02d}{d:02d}_Data_run-276243_SingleMu_CHUNK0'.format(
            y=TODAY.tm_year, m=TODAY.tm_mon, d=TODAY.tm_mday),
        'Turnons'
    )
    main(10000, output_folder)
