from __future__ import print_function
from rootpy.tree import TreeChain
import six
# import inspect
import math

from jetfilters import defaultJetFilter


class Event(object):

    def __init__(self, trees):
        self._trees = trees
        # add names, aliases?
        # lets assume fixed for now:
        self._caloTower, self._emuCaloTower, self._jetReco,\
            self._metFilterReco, self._muonReco, self._recoTree,\
            self._upgrade, self._emuUpgrade = self._trees

        self._jets = []
        for i in range(self._jetReco.Jet.nJets):
            self._jets.append(Jet(self._jetReco.Jet, i))

    def test(self):
        # for tree in self._trees:
        #     print(tree)
        print('>>>> nHCALTP', self._caloTower.CaloTP.nHCALTP)
        print('>>>> nHCALTP (emu)', self._emuCaloTower.CaloTP.nHCALTP)
        print('>>>> nJets', self._jetReco.Jet.nJets)
        print('>>>> met', self._jetReco.Sums.met)
        print('>>>> hbheNoiseFilter',
              self._metFilterReco.MetFilters.hbheNoiseFilter)
        print('>>>> nMuons', self._muonReco.Muon.nMuons)
        print('>>>> nVtx', self._recoTree.Vertex.nVtx)
        print('>>>> nJets (upgrade)', self._upgrade.L1Upgrade.nJets)
        print('>>>> nJets (upgrade emu)', self._emuUpgrade.L1Upgrade.nJets)
        print(self._jets[0].eta)
        print('>>>> Leading reco jet ET', self.getLeadingRecoJet().etCorr)
        print('>>>> Lowest good jet ET', self.goodJets()[-1].etCorr)

        # print(dir(self._jetReco.Jet))
        # members = inspect.getmembers(self._jetReco.Jet)
        # print('>>>> Jet members')
        # for m in members:
        #     print('>' * 6, m[0], ':', m[1])

    def goodJets(self, jetFilter=defaultJetFilter):
        '''
            filters and ET orders the jet collection
        '''
        goodJets = filter(jetFilter, self._jets)
        sorted_jets = sorted(
            goodJets, key=lambda jet: jet.etCorr, reverse=True)
        return sorted_jets

    def getLeadingRecoJet(self, jetFilter=defaultJetFilter):
        goodJets = self.goodJets(jetFilter)
        if not goodJets:
            return None
        leadingRecoJet = goodJets[0]
        if leadingRecoJet.etCorr > 10.0:
            return leadingRecoJet
        return None

    def getMatchedL1Jet(self, recoJet, l1Type='HW'):
        l1Jets = None
        if l1Type == 'HW':
            l1Jets = [L1Jet(self._upgrade.L1Upgrade, i)
                      for i in range(self._upgrade.L1Upgrade.nJets)]
        if l1Type == 'EMU':
            l1Jets = [L1Jet(self._emuUpgrade.L1Upgrade, i)
                      for i in range(self._emuUpgrade.L1Upgrade.nJets)]

        if not l1Jets or not recoJet:
            return None
        minDeltaR = 0.3
        closestJet = None
        for l1Jet in l1Jets:
            dEta = recoJet.eta - l1Jet.eta
            dPhi = recoJet.phi - l1Jet.phi
            dR = math.sqrt(dEta**2 + dPhi**2)
            if dR < minDeltaR:
                minDeltaR = dR
                closestJet = l1Jet
        return closestJet

    @property
    def nVertex(self):
        return self._recoTree.Vertex.nVtx


class Jet(object):
    '''
        Create a simple python wrapper for
        L1Analysis::L1AnalysisRecoJetDataFormat
    '''

    def __init__(self, jets, index):
        # this could be simplified with a list of attributes
        read_attributes = [
            'etCorr', 'muMult', 'eta', 'phi', 'nhef', 'pef', 'mef', 'chMult',
            'elMult', 'nhMult', 'phMult', 'chef', 'eef'
        ]
        for attr in read_attributes:
            setattr(self, attr, getattr(jets, attr)[index])

    @property
    def sumMult(self):
        return self.chMult + self.chMult + self.elMult
        # not
        # return self.chMult + self.muMult + self.elMult ?

    @property
    def allMult(self):
        return self.sumMult + self.nhMult + self.phMult


class L1Jet(object):

    def __init__(self, l1Jets, index):
        self.et = l1Jets.jetEt[index]
        self.eta = l1Jets.jetEta[index]
        self.phi = l1Jets.jetPhi[index]


class EventReader(object):

    def __init__(self, tree_names, files):
        # this is not efficient
        self._trees = [TreeChain(name, files) for name in tree_names]

    def __iter__(self):
        for trees in six.moves.zip(*self._trees):
            yield Event(trees)


if __name__ == '__main__':
    import glob
    import ROOT
    ROOT.gSystem.Load('build/L1TAnalysisDataformats.so')
    files = glob.glob('data/*.root')
    tree_names = [
        'l1CaloTowerTree/L1CaloTowerTree',
        'l1CaloTowerEmuTree/L1CaloTowerTree',
        'l1JetRecoTree/JetRecoTree',
        'l1MetFilterRecoTree/MetFilterRecoTree',
        'l1MuonRecoTree/Muon2RecoTree',
        'l1RecoTree/RecoTree',
        'l1UpgradeEmuTree/L1UpgradeTree',
        'l1UpgradeTree/L1UpgradeTree',
    ]

    reader = EventReader(tree_names, files)
    i = 1
    for event in reader:
        print('-' * 80)
        print('>> event', i)
        event.test()
        print('-' * 80)
        i += 1
        if i > 3:
            break
