

# Alpha 0.1.0
 - [x] Include Shane's macros as 'legacy' for comparison
 - [x] Read L1TNtuples in python
 - [x] Transfer 1 Macro to python (makeJetResolutions)
 - [x] Benchmark legacy vs new
 - [x] Add histogram collections for easier creation & handling
   - [x] Added multidimensional dictionary based on defaultdict
  custom dicts or objects in certain dimensions
   - [x] Added HistogramByPileUpCollection
     - [x] Automatic selection of PU bin based on pileup value. E.g. `histograms[11]` will fill the 2nd bin if `pileupBins=[0,10,20,30,999]`
   - [x] Added ResolutionCollection
     - [x] Specialisation of HistogramByPileUpCollection
     - [x] Automatic selection of detector region based on `cmsl1t.geometry`
 - [x] Implement Ben's MET turnons to check if the package is going the right way
 - [x] Explore ways to recalculate MET
 - [x] Implement EfficiencyCollection
 - [x] First PR to main repo
 - [x] Request feedback from other analysers
   - [x] See what is easy, what is not
