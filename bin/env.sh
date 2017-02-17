#!/bin/bash

source /cvmfs/grid.cern.ch/etc/profile.d/setup-cvmfs-ui.sh
# ROOT 6, voms-proxy-init and other things
# this ROOT version is not compiled with xrootd bindings (might become a problem)!
source /cvmfs/sft.cern.ch/lcg/views/LCG_latest/x86_64-slc6-gcc62-opt/setup.sh

# to fix java for the hadoop commands:
unset JAVA_HOME

git submodule init
git submodule update
