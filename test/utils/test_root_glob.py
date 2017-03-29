import unittest
from cmsl1t.utils.root_glob import glob as root_glob
import glob as py_glob


class TestGlob(unittest.TestCase):

    def test_glob_local_single(self):
        filename = "data/L1Ntuple_test_3.root"
        self.assertEqual([filename], root_glob(filename))

    def test_glob_local_wildcard(self):
        filename = "data/*root"
        self.assertEqual(root_glob(filename), py_glob(filename))

#    def test_glob_xrootd_single(self):
#       filename = """root://eoscms.cern.ch//eos/cms/store/group/"""
#       """dpg_trigger/comm_trigger/L1Trigger/L1Menu2016/Stage2/"""
#       """l1t-integration-v88p1-CMSSW-8021/SingleMuon/"""
#       """crab_l1t-integration-v88p1-CMSSW-8021__SingleMuon_2016H_v2/"""
#       """161031_120512/0000/L1Ntuple_999.root""",

#    def test_glob_xrootd_wildcard(self):
#       filename = """root://eoscms.cern.ch//eos/cms/store/group/"""
#       """dpg_trigger/comm_trigger/L1Trigger/L1Menu2016/Stage2/"""
#       """l1t-integration-v88p1-CMSSW-8021/SingleMuon/"""
#       """crab_l1t-integration-v88p1-CMSSW-8021__SingleMuon_2016H_v2/"""
#       """161031_120512/0000/L1Ntuple_99*.root"""
