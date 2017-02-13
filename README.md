# cms-l1t-analysis
Software package to analyse L1TNtuples


## DEV
```bash
git clone https://github.com/<your github user name>/cms-l1t-analysis.git
cd cms-l1t-analysis
git remote add upstream https://github.com/cms-l1t-offline/cms-l1t-analysis.git
vagrant up
vagrant ssh
cd /vagrant
source bin/env.sh
# you will need your grid cert
voms-proxy-init --voms cms

```
