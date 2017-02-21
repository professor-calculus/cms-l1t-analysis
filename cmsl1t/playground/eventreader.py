from __future__ import print_function
from rootpy.tree import Tree, TreeChain
#from six.moves import zip
import six


class Event(object):

    def __init__(self, trees):
        self._trees = trees
        # add names, aliases?

    def test(self):
        # for tree in self._trees:
        #     print(tree)
        print('>>>> nHCALTP', self._trees[0].CaloTP.nHCALTP)
        print('>>>> nHCALTP (emu)', self._trees[1].CaloTP.nHCALTP)
        print('>>>> nJets', self._trees[2].Jet.nJets)
        print('>>>> met', self._trees[2].Sums.met)
        print('>>>> hbheNoiseFilter', self._trees[3].MetFilters.hbheNoiseFilter)
        print('>>>> nMuons', self._trees[4].Muon.nMuons)
        print('>>>> nVtx', self._trees[5].Vertex.nVtx)
        print('>>>> nJets (upgrade emu)', self._trees[6].L1Upgrade.nJets)
        print('>>>> nJets (upgrade)', self._trees[7].L1Upgrade.nJets)


class EventReader(object):

    def __init__(self, trees, files):
        self._tree_names = trees
        self._files = files
        self._trees = []
        for name in self._tree_names:
            # this is not efficient
            self._trees.append(TreeChain(name, self._files))

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
        print('-'*80)
        print('>> event', i)
        event.test()
        print('-'*80)
        i += 1
        if i > 3:
            break
