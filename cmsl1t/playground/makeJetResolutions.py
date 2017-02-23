import ROOT
import os
from rootpy.plotting import Hist
import glob
import six
import math
import numpy as np
import logging
from eventreader import EventReader

logging.getLogger("rootpy.tree.chain").setLevel(logging.WARNING)


FILES = glob.glob('data/*.root')
TREE_NAMES = [
    'l1CaloTowerTree/L1CaloTowerTree',
    'l1CaloTowerEmuTree/L1CaloTowerTree',
    'l1JetRecoTree/JetRecoTree',
    'l1MetFilterRecoTree/MetFilterRecoTree',
    'l1MuonRecoTree/Muon2RecoTree',
    'l1RecoTree/RecoTree',
    'l1UpgradeEmuTree/L1UpgradeTree',
    'l1UpgradeTree/L1UpgradeTree',
]


def main(nEvents, output_folder):
    ROOT.PyConfig.IgnoreCommandLineOptions = True
    ROOT.gROOT.SetBatch(1)
    ROOT.TH1.SetDefaultSumw2(True)
    ROOT.gStyle.SetOptStat(0)
    energy_bins = np.arange(-1, 1.5, 0.05)
    position_bins = np.arange(-0.3, 0.3, 0.005)
    histograms = {
        'JetEtHF': Hist(energy_bins, name='JetEtHF'),
        'JetEtB': Hist(energy_bins, name='JetEtB'),
        'JetEtBE': Hist(energy_bins, name='JetEtBE'),
        'JetEtE': Hist(energy_bins, name='JetEtF'),
        #
        'JetEtaHF': Hist(position_bins, name='JetEtaHF'),
        'JetEtaB': Hist(position_bins, name='JetEtaB'),
        'JetEtaBE': Hist(position_bins, name='JetEtaBE'),
        'JetEtaE': Hist(position_bins, name='JetEtaE'),
        #
        'JetPhiHF': Hist(position_bins, name='JetPhiHF'),
        'JetPhiB': Hist(position_bins, name='JetPhiB'),
        'JetPhiBE': Hist(position_bins, name='JetPhiBE'),
        'JetPhiE': Hist(position_bins, name='JetPhiE'),
    }

    reader = EventReader(TREE_NAMES, FILES)

    for entry, event in enumerate(reader):
        if entry >= nEvents:
            break

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

        if abs(recoEta) <= 1.479:
            histograms['JetEtB'].Fill(resolution_et)
            histograms['JetEtBE'].Fill(resolution_et)
            histograms['JetEtaB'].Fill(resolution_eta)
            histograms['JetEtaBE'].Fill(resolution_eta)
            histograms['JetPhiB'].Fill(resolution_phi)
            histograms['JetPhiBE'].Fill(resolution_phi)
        elif abs(recoEta) <= 3.0:
            histograms['JetEtBE'].Fill(resolution_et)
            histograms['JetEtE'].Fill(resolution_et)
            histograms['JetEtaBE'].Fill(resolution_eta)
            histograms['JetEtaE'].Fill(resolution_eta)
            histograms['JetPhiBE'].Fill(resolution_phi)
            histograms['JetPhiE'].Fill(resolution_phi)
        else:
            if recoEt >= 30. and l1Et != 0:
                histograms['JetEtHF'].Fill(resolution_et)
                histograms['JetEtaHF'].Fill(resolution_eta)
                histograms['JetPhiHF'].Fill(resolution_phi)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for name, hist in six.iteritems(histograms):
        file_name = 'res_SingleMu_reco{name}_l1{name}'.format(name=name)
        canvas_name = file_name.replace('SingleMu', 'Energy')
        if 'JetEta' in name or 'JetPhi' in name:
            canvas_name.replace('Energy', 'Position')
        c = ROOT.TCanvas(canvas_name)
        hist.Draw()
        c.SaveAs(os.path.join(output_folder, file_name + '.pdf'))
        c.SaveAs(os.path.join(output_folder, file_name + '.root'))


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
