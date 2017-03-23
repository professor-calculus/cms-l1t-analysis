# Introduction / Background / Context / etc
The existing code used for analysis of L1 Trigger:
https://github.com/shane-breeze/l1t-macros

#### Issues and scopes for improvement
 - Adding a new plot or studying some new variable requires writing a lot of extra code
 - Code is all written as ROOT “C++” macros which (in this case) cannot be compiled, making debugging rather hard

#### In its current form it is configured to plot
 - L1 object efficiency (wrt gen, wrt RECO) as function of pT, eta, phi
 - L1 object rate as function of threshold
 - Object distributions in pT, eta, phi, isolation, other stuff (L1, gen, RECO objects) 
 - L1 object resolutions (wrt gen, wrt RECO) in pT, eta, phi
 - Efficiency vs. Rate

Plots are typically "binned" by pile-up and other variables, so that in addition to binning along the X and Y axes,
multiple plots are produced depending on a third variable, eg. number of reconstructed vertices in the event (pile-up).
The final plots then contain multiple curves, one for each of these bins.

Current command for data or MC:
From top-level of l1t-macros:

```bash
root -l -b -q MakePlots/makeRates.cxx'(0,1,1000,0)'
```

#### Typical Use Cases (though I’m not sure these are really ‘use’ cases, more requirements)
 - Analysis tasks
 - Produce ‘default’ or ‘standard’ set of plots for a new set of data
 - Produce ‘default’ or ‘standard’ set of plots over a subset of data, where subset could be specified by a cut on a variable, a run number, trigger condition, etc
 - Produce default plots, but recompute the objects entering it (eg. change an object algorithm, re-calibrate, change thresholds etc.)
 - Add a new type of plot
 - Inspect existing plots using different binning
 - Change plot cosmetics some time after plots originally produced (eg. conferences)
 - Produce hardware vs emulator comparisons for all L1 objects (for validation events)

#### Input Data Sources and Format
 - The input data consists of L1TNtuples
 - The input data is typically stored under `/eos/cms/store/group/dpg_trigger/comm_trigger/`  [*The current code seems to use xrootd to access these files from eoscms.cern.ch*]
 - Typical number of events to process for a full analysis: > 1m
 - May want to be able to read back in root plots 

#### Running
 - User runs locally on lxplus
 - User runs on HTCondor batch systems
 - User runs locally from another institution’s login computer
 - User runs on their laptop
 - [Could consider batch systems, etc]

#### Implementation Considerations
 - Language:
 - Python
 - C++
 - YAML / JSON-based config files
 - <small>Mixed  approach -- analysis loop in c++, configuration via python wrapped command</small>

#### Run-time configurable options (provided eg. via the command line or in a config file)
 - Output directory for plots etc
 - Input data
 - Plot binning

#### Command invocation options
 - <cmd> [options] configfile.cfg
 - <cmd> [options[ options[ options]]]
