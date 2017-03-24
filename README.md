# cms-l1t-analysis
Software package to analyse L1TNtuples

 - [![Build Status](https://travis-ci.org/cms-l1t-offline/cms-l1t-analysis.svg?branch=master)](https://travis-ci.org/cms-l1t-offline/cms-l1t-analysis)
 - [![DOI](https://zenodo.org/badge/80877637.svg)](https://zenodo.org/badge/latestdoi/80877637)


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
make setup
```

### running benchmark
```
# install python requirements
pip install -r requirements.txt --user
make benchmark
```
