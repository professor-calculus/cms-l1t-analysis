#!/bin/bash
PROJECT_NAME="cms-l1t-analysis"

if [ -n "${PROJECT_ROOT}" ] ; then
   old_projectbase=${PROJECT_ROOT}
fi

if [ "x${BASH_ARGV[0]}" = "x" ]; then
    if [ ! -f bin/env.sh ]; then
        echo ERROR: must "cd where/${PROJECT_NAME}/is" before calling ". bin/env.sh" for this version of bash!
        PROJECT_ROOT=; export PROJECT_ROOT
        return 1
    fi
    PROJECT_ROOT="$PWD"; export PROJECT_ROOT
else
    # get param to "."
    envscript=$(dirname ${BASH_ARGV[0]})
    PROJECT_ROOT=$(cd ${envscript}/..;pwd); export PROJECT_ROOT
fi

# clean PATH and PYTHONPATH
if [ -n "${old_projectbase}" ] ; then
  PATH=`python ${PROJECT_ROOT}/bin/remove_from_env.py "$PATH" "${old_projectbase}"`
  PYTHONPATH=`python ${PROJECT_ROOT}/bin/remove_from_env.py "$PYTHONPATH" "${old_projectbase}"`
fi

# add project to PYTHONPATH
if [ -z "${PYTHONPATH}" ]; then
   PYTHONPATH=${PROJECT_ROOT}; export PYTHONPATH
else
   PYTHONPATH=${PROJECT_ROOT}:$PYTHONPATH; export PYTHONPATH
fi

unset old_projectbase
unset envscript

# this gives you voms-proxy-*, xrdcp and other grid tools
source /cvmfs/grid.cern.ch/etc/profile.d/setup-cvmfs-ui.sh
# ROOT 6, voms-proxy-init and other things
source /cvmfs/sft.cern.ch/lcg/views/LCG_latest/x86_64-slc6-gcc62-opt/setup.sh

# to fix java for the hadoop commands:
unset JAVA_HOME


git submodule init
git submodule update
pip install --user -r requirements.txt

echo "Environment for ${PROJECT_NAME} is ready"
