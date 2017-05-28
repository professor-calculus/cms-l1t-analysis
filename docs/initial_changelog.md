## details of first-draft
 - Include Shane's macros as 'legacy' for comparison
 - Read L1TNtuples in python
 - Transfer 1 Macro to python (makeJetResolutions)
 - Benchmark legacy vs new
 - Add histogram collections for easier creation & handling
   - Added multidimensional dictionary based on defaultdict
  custom dicts or objects in certain dimensions
   - Added HistogramByPileUpCollection
     - Automatic selection of PU bin based on pileup value. E.g. `histograms[11]` will fill the 2nd bin if `pileupBins=[0,10,20,30,999]`
   - Added ResolutionCollection
     - Specialisation of HistogramByPileUpCollection
     - Automatic selection of detector region based on `cmsl1t.geometry`
 - Implement Ben's MET turnons to check if the package is going the right way
 - Explore ways to recalculate MET
 - Implement EfficiencyCollection
 - First PR to main repo
 - Request feedback from other analysers
   - See what is easy, what is not
