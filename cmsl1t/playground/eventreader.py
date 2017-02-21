from __future__ import print_function
from rootpy.tree import Tree, TreeChain
#from six.moves import zip
import six


class Event(object):

    def __init__(self, trees):
        self._trees = trees
        # add names, aliases?
        # lets assume fixed for now:
        self._caloTower, self._emuCaloTower, self._jetReco, self._metFilterReco,\
            self._muonReco, self._recoTree, self._upgrade, self._emuUpgrade = self._trees

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
        print('>>>> nJets (upgrade emu)', self._upgrade.L1Upgrade.nJets)
        print('>>>> nJets (upgrade)', self._emuUpgrade.L1Upgrade.nJets)

    def getLeadingRecoJet(self):
        pass


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
