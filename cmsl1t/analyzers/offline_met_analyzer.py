"""
Make plots for offline met studies
"""

from BaseAnalyzer import BaseAnalyzer
from cmsl1t.plotting.efficiency import EfficiencyPlot
from cmsl1t.plotting.onlineVsOffline import OnlineVsOffline
from cmsl1t.plotting.resolution import ResolutionPlot
from cmsl1t.plotting.resolution_vs_X import ResolutionVsXPlot
import cmsl1t.recalc.met as recalc
from cmsl1t.playground.eventreader import Met, Sum
from math import pi
import pprint
from collections import namedtuple
import numpy as np


sum_types = ["HTT", "MHT", "MET_HF", "MET_noHF", "MET_PF", "MET_PF_NoMu", "MET_PF_HF", "MET_PF_NoMu_HF"]
Sums = namedtuple("Sums", sum_types)


def ExtractSums(event):
    offline = dict(HTT=Sum(event.sums.Ht),
                   MHT=Met(event.sums.mHt, event.sums.mHtPhi),
                   MET_HF=Met(event.sums.caloMet, event.sums.caloMetPhi),
                   MET_noHF=Met(event.sums.caloMetBE, event.sums.caloMetPhiBE),
                   MET_PF=Met(event.sums.met, event.sums.metPhi),
                   MET_PF_NoMu=Met(event.sums.pfMetNoMu, event.sums.pfMetNoMuPhi),
                   MET_PF_HF=Met(event.sums.met, event.sums.metPhi),
                   MET_PF_NoMu_HF=Met(event.sums.pfMetNoMu, event.sums.pfMetNoMuPhi)
                   )
    online = dict(HTT=event.l1Sums["L1Htt"],
                  MHT=event.l1Sums["L1Mht"],
                  MET_HF=event.l1Sums["L1MetHF"],
                  MET_noHF=event.l1Sums["L1Met"],
                  MET_PF=event.l1Sums["L1Met"],
                  MET_PF_NoMu=event.l1Sums["L1Met"],
                  MET_PF_HF=event.l1Sums["L1MetHF"],
                  MET_PF_NoMu_HF=event.l1Sums["L1MetHF"]
                  )
    return online, offline


class Analyzer(BaseAnalyzer):
    def __init__(self, config, **kwargs):
        super(Analyzer, self).__init__("offline_met_analyzer", config)

        for name in sum_types:
            eff_plot = EfficiencyPlot("online" + name, "offline" + name)
            res_plot = ResolutionPlot("energy", "online" + name, "offline" + name)
            twoD_plot = OnlineVsOffline("online" + name, "offline" + name)
            self.register_plotter(eff_plot)
            self.register_plotter(res_plot)
            self.register_plotter(twoD_plot)
            setattr(self, name + "_eff", eff_plot)
            setattr(self, name + "_res", res_plot)
            setattr(self, name + "_2D", twoD_plot)

            eff_plot_HR = EfficiencyPlot("online" + name, "offline" + name + "_HiRange")
            res_plot_HR = ResolutionPlot("energy", "online" + name, "offline" + name + "_HiRange")
            twoD_plot_HR = OnlineVsOffline("online" + name, "offline" + name + "_HiRange")
            self.register_plotter(eff_plot_HR)
            self.register_plotter(res_plot_HR)
            self.register_plotter(twoD_plot_HR)
            setattr(self, name + "_eff_HR", eff_plot_HR)
            setattr(self, name + "_res_HR", res_plot_HR)
            setattr(self, name + "_2D_HR", twoD_plot_HR)

        for angle in sum_types[1:]:
            name = angle + "_phi"
            res_plot = ResolutionPlot("phi", "online" + name, "offline" + name)
            twoD_plot = OnlineVsOffline("online" + name, "offline" + name)
            self.register_plotter(res_plot)
            self.register_plotter(twoD_plot)
            setattr(self, name + "_res", res_plot)
            setattr(self, name + "_2D", twoD_plot)

            res_plot_HR = ResolutionPlot("phi", "online" + name, "offline" + name + "_HiRange")
            twoD_plot_HR = OnlineVsOffline("online" + name, "offline" + name + "_HiRange")
            self.register_plotter(res_plot_HR)
            self.register_plotter(twoD_plot_HR)
            setattr(self, name + "_res_HR", res_plot_HR)
            setattr(self, name + "_2D_HR", twoD_plot_HR)

        self.res_vs_eta_CentralJets = ResolutionVsXPlot("energy", "onlineJet", "offlineJet", "offlineJet_eta")
        self.register_plotter(self.res_vs_eta_CentralJets)

    def prepare_for_events(self, reader):
        # TODO: Get these from a common place, and / or the config file
        puBins = range(0, 50, 10) + [999]
        thresholds = [40, 60, 80, 100, 120]
        thresholds2 = [160, 220, 280, 340, 400]
        tmpbins1 = range(0, 410, 10)
        tmpbins2 = range(450, 1050, 50)
        tmpbins3 = range(1100, 2100, 100)
        tmpbins1.extend(tmpbins2)
        tmpbins1.extend(tmpbins3)
        xbins = np.asarray(tmpbins1, 'd')    #The 'd' arg is vital here, else it will claim axis length zero...


        Config = namedtuple("Config", "name off_title on_title off_max on_max")
        HTT_cfg = Config("HTT", "Offline HTT", "L1 HTT", 600, 600)
        MHT_cfg = Config("MHT", "Offline MHT", "L1 MHT", 400, 400)
        MET_HF_cfg = Config("MET_HF", "Offline MET with HF", "L1 MET", 400, 400)
        MET_noHF_cfg = Config("MET_noHF", "Offline MET no HF", "L1 MET", 400, 400)
        MET_PF_cfg = Config("MET_PF", "Offline PF MET", "L1 MET", 400, 400)
        MET_PF_NoMu_cfg = Config("MET_PF_NoMu", "Offline PF MET without Muons", "L1 MET", 400, 400)
        MET_PF_HF_cfg = Config("MET_PF_HF", "Offline PF MET with HF", "L1 MET", 400, 400)
        MET_PF_NoMu_HF_cfg = Config("MET_PF_NoMu_HF", "Offline PF MET with HF without Muons", "L1 MET", 400, 400)
        HTT_cfg_HR = Config("HTT", "Offline HTT", "L1 HTT", 2000, 2000)
        MHT_cfg_HR = Config("MHT", "Offline MHT", "L1 MHT", 2000, 2000)
        MET_HF_cfg_HR = Config("MET_HF", "Offline MET with HF", "L1 MET", 2000, 2000)
        MET_noHF_cfg_HR = Config("MET_noHF", "Offline MET no HF", "L1 MET", 2000, 2000)
        MET_PF_cfg_HR = Config("MET_PF", "Offline PF MET", "L1 MET", 2000, 2000)
        MET_PF_NoMu_cfg_HR = Config("MET_PF_NoMu", "Offline PF MET without Muons", "L1 MET", 2000, 2000)
        MET_PF_HF_cfg_HR = Config("MET_PF_HF", "Offline PF MET with HF", "L1 MET", 2000, 2000)
        MET_PF_NoMu_HF_cfg_HR = Config("MET_PF_NoMu_HF", "Offline PF MET with HF without Muons", "L1 MET", 2000, 2000)
        cfgs = [HTT_cfg, MHT_cfg, MET_HF_cfg, MET_noHF_cfg, MET_PF_cfg, MET_PF_NoMu_cfg, MET_PF_HF_cfg, MET_PF_NoMu_HF_cfg]
        cfgs2 = [HTT_cfg_HR, MHT_cfg_HR, MET_HF_cfg_HR, MET_noHF_cfg_HR, MET_PF_cfg_HR, MET_PF_NoMu_cfg_HR, MET_PF_HF_cfg_HR, MET_PF_NoMu_HF_cfg_HR]
        for cfg in cfgs:
            eff_plot = getattr(self, cfg.name + "_eff")
            res_plot = getattr(self, cfg.name + "_res")
            twoD_plot = getattr(self, cfg.name + "_2D")
            eff_plot.build(cfg.on_title + " (GeV)", cfg.off_title + " (GeV)",
                           puBins, thresholds, 50, 0, cfg.off_max)
            twoD_plot.build(cfg.on_title + " (GeV)", cfg.off_title + " (GeV)",
                            puBins, 50, 0, cfg.off_max)
            res_plot.build(cfg.on_title, cfg.off_title,
                           puBins, 50, -10, 10)

            if not hasattr(self, cfg.name + "_phi_res"):
                continue
            res_plot = getattr(self, cfg.name + "_phi_res")
            twoD_plot = getattr(self, cfg.name + "_phi_2D")
            twoD_plot.build(cfg.on_title + " Phi (rad)", cfg.off_title + " Phi (rad)",
                            puBins, 50, -pi, 2 * pi)
            res_plot.build(cfg.on_title + " Phi", cfg.off_title + " Phi",
                           puBins, 50, -2, 2)

        for cfg in cfgs2:
            eff_plot_HR = getattr(self, cfg.name + "_eff_HR")
            res_plot_HR = getattr(self, cfg.name + "_res_HR")
            twoD_plot_HR = getattr(self, cfg.name + "_2D_HR")
            eff_plot_HR.build(cfg.on_title + " (GeV)", cfg.off_title + " (GeV)",
                           puBins, thresholds, xbins.size - 1, xbins)
            twoD_plot_HR.build(cfg.on_title + " (GeV)", cfg.off_title + " (GeV)",
                            puBins, 200, 0, cfg.off_max)
            res_plot_HR.build(cfg.on_title, cfg.off_title,
                           puBins, 50, -10, 10)

            if not hasattr(self, cfg.name + "_phi_res_HR"):
                continue
            res_plot_HR = getattr(self, cfg.name + "_phi_res_HR")
            twoD_plot_HR = getattr(self, cfg.name + "_phi_2D_HR")
            twoD_plot_HR.build(cfg.on_title + " Phi (rad)", cfg.off_title + " Phi (rad)",
                            puBins, 50, -pi, 2 * pi)
            res_plot_HR.build(cfg.on_title + " Phi", cfg.off_title + " Phi",
                           puBins, 50, -2, 2)

        self.res_vs_eta_CentralJets.build("Online Jet energy (GeV)",
                                          "Offline Jet energy (GeV)", "Offline Jet Eta (rad)",
                                          puBins, 50, -0.5, 3.5, 50, -5., 5.)
        return True

    def fill_histograms(self, entry, event):
        if not event.passesMETFilter():
            return True

        offline, online = ExtractSums(event)
        pileup = event.nVertex

        for name in sum_types:
            on = online[name]
            if on.et == 0:
                continue
            off = offline[name]
            getattr(self, name + "_eff").fill(pileup, off.et, on.et)
            getattr(self, name + "_res").fill(pileup, off.et, on.et)
            getattr(self, name + "_2D").fill(pileup, off.et, on.et)
            getattr(self, name + "_eff_HR").fill(pileup, off.et, on.et)
            getattr(self, name + "_res_HR").fill(pileup, off.et, on.et)
            getattr(self, name + "_2D_HR").fill(pileup, off.et, on.et)
            if hasattr(self, name + "_phi_res"):
                getattr(self, name + "_phi_res").fill(pileup, off.phi, on.phi)
                getattr(self, name + "_phi_2D").fill(pileup, off.phi, on.phi)
                getattr(self, name + "_phi_res_HR").fill(pileup, off.phi, on.phi)
                getattr(self, name + "_phi_2D_HR").fill(pileup, off.phi, on.phi)

        for recoJet in event.goodJets():
            l1Jet = event.getMatchedL1Jet(recoJet)
            if not l1Jet:
                continue
            self.res_vs_eta_CentralJets.fill(pileup, recoJet.eta, recoJet.etCorr, l1Jet.et)

        return True
