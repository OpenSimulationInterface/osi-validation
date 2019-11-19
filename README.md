# OSI Validator
[![Travis Build Status](https://travis-ci.org/OpenSimulationInterface/osi-validation.svg?branch=master)](https://travis-ci.org/OpenSimulationInterface/osi-validation)

OSI Validator checks the compliance of OSI messages with predefined [rules](https://opensimulationinterface.github.io/osi-documentation/osi-validation/doc/osivalidator.html#module-osivalidator.osi_rules_implementations). The full documentation on the validator and customization of the rules is available [here](https://opensimulationinterface.github.io/osi-documentation/osi-validation/README.html).

## Usage

```
usage: osivalidator [-h] [--rules RULES] --data DATA
                    [--type {SensorView,GroundTruth,SensorData}]
                    [--output OUTPUT] [--timesteps TIMESTEPS] [--debug]
                    [--verbose]

Validate data defined at the input

optional arguments:
--help, -h                                      Show this help message and exit.
--rules RULES, -r RULES                         Directory with text files containig rules.
--data DATA, -d DATA                            Path to the file with OSI-serialized data.
--type {SensorView,GroundTruth,SensorData},     Name of the message type used to serialize data.
    -t {SensorView,GroundTruth,SensorData}
--output OUTPUT, -o OUTPUT                      Output folder of the log files.
--timesteps TIMESTEPS                           Number of timesteps to analyze. If -1, all.
--debug                                         Set the debug mode to ON.
--verbose                                       Set the verbose mode to ON (display in console).
```

## Installation

OSI Validator has been developed with Python 3.6 within a virtual environment on Ubuntu 18.04.

#### Local (recommended)

```bash
$ git clone https://github.com/OpenSimulationInterface/osi-validation.git
$ cd osi-validation
$ git clone https://github.com/OpenSimulationInterface/open-simulation-interface.git
$ git clone https://github.com/OpenSimulationInterface/proto2cpp.git
$ sudo apt-get install virtualenv
$ virtualenv -p /usr/bin/python3 vpython
$ source vpython/bin/activate
$ cd open-simulation-interface
$ pip install .
$ cd ..
$ pip install .
```

#### Global

```bash
$ git clone https://github.com/OpenSimulationInterface/osi-validation.git
$ cd osi-validation
$ git clone https://github.com/OpenSimulationInterface/proto2cpp.git
$ git clone https://github.com/OpenSimulationInterface/open-simulation-interface.git
$ cd open-simulation-interface
$ sudo pip3 install .
$ cd ..
$ sudo pip3 install .
```