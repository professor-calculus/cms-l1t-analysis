```
res[pu]['jetEt'][region].fill(jet.et()) > res.fill('jetEt', jet.et())
```


```
hists = MyHistCollection(pileupBins=[0, 13, 20, 999])
hists.add_variable('jetEt')
with Session(events, hists=[...]) as s:
with Session(cfg) as s:
    # expert defined
    s.run()

for event in events:
    # should this be implicit
    # hists.set_pu(pu)
    with Session(event, hists=[hists]) as s:
      s.fill(hists, 'jets[0].et()', ....)
      hists[22][region]['jetEt'].fill(events.jets[0].et())
```
Separate event loop and code to run
user defined function:
```
def myThing(event)
```

```yaml

files:
  - /eos/..../*.root
modifiers:
  recalcMET:
    func: cmsl1t.recalc.recalcMET
    in: event.caloTowers
    out: recalcMET
    kwargs:
      another: 42
      lut_file: /eos/..../myFile.lut
    args:
      - 4234
      - vksdfj

histograms:
  Resolution:
    pile_up_bins: 0, 13, 20, 999
    variables:
      - jetEt: 'jets[0].et()'
      - jetEtvsEta:
          - 'jets[0].et()'
          - 'jets[0].eta()'
      - recalcMET: recalcMET
    filters:
      MyEventFilter:
        worksOn: event
        requires:
          met: '> 20'
  Efficiency:
    variables:
      - jetEt:
        - reco: 'jets[0].et()'
        - l1: 'l1Jets[0].et()'
        - thresholds: 20, 30, 50, 100, 200
  Rates:
