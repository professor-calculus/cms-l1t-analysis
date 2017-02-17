import ROOT
import os
import rootpy
from rootpy.io import root_open
from rootpy.tree import Tree
import glob

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(1)
ROOT.TH1.SetDefaultSumw2(True)
ROOT.gStyle.SetOptStat(0)

ROOT.gSystem.Load('build/L1TAnalysisDataformats.so')

f = root_open("data/L1Ntuple_test.root")

tree = f.Get("l1EventTree/L1EventTree")
for entry, event in enumerate(tree):
    print(event.Event.event)
    if entry > 100:
        break
