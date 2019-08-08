#!/bin/sh
git clone https://github.com/vkresch/osi-validation.git;
cd osi-validation;
git checkout development;
git clone https://github.com/OpenSimulationInterface/open-simulation-interface.git;
git clone https://github.com/OpenSimulationInterface/proto2cpp.git;
sudo apt-get install virtualenv;
virtualenv -p /usr/bin/python3 vpython;
source vpython/bin/activate;
cd open-simulation-interface; pip install .;
pip install -r requirements.txt;
cd ..; pip install .;
cp -R requirements-osi-3 vpython/lib/python3.6/site-packages/;
