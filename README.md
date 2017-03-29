# cms-l1t-analysis
Software package to analyse L1TNtuples

 - [![Build Status](https://travis-ci.org/cms-l1t-offline/cms-l1t-analysis.svg?branch=master)](https://travis-ci.org/cms-l1t-offline/cms-l1t-analysis)
 - [![DOI](https://zenodo.org/badge/80877637.svg)](https://zenodo.org/badge/latestdoi/80877637)


## DEV

 1. Fork the project on https://github.com/cms-l1t-offline/cms-l1t-analysis
 2. Follow the instructions below

### On Scientific Linux 6 with CVMFS available
This includes nodes lxplus.cern.ch & private clusters
```bash
git clone https://github.com/<your github user name>/cms-l1t-analysis.git
cd cms-l1t-analysis
git remote add upstream https://github.com/cms-l1t-offline/cms-l1t-analysis.git
source bin/env.sh
# you will need your grid cert
voms-proxy-init --voms cms
make setup
```

### On OS X/other Linux/Windows
 1. Install [Virtualbox](https://www.virtualbox.org/wiki/Downloads)
 2. Install [Vagrant](https://www.vagrantup.com/downloads.html)
   - You might need to also install `vagrant-libvirt` on some systems if you see "The provider 'libvirt' could not be found, but was requested to
back the machine 'default'. Please use a provider that exists."
 3. Follow instructions below
```bash
git clone https://github.com/<your github user name>/cms-l1t-analysis.git
cd cms-l1t-analysis
git remote add upstream https://github.com/cms-l1t-offline/cms-l1t-analysis.git
# only on non Scientific Linux machines (e.g. OS X, Windows, Ubuntu, etc)
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

### Generating changelog
```bash
make changelog
```

#### Prerequisites
```bash
gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
\curl -sSL https://get.rvm.io | bash -s stable --ruby
source ~/.rvm/scripts/rvmsource ~/.rvm/scripts/rvm
gem install github_changelog_generator
```
