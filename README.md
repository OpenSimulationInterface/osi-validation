# OSI Validator
[![Travis Build Status](https://travis-ci.com/OpenSimulationInterface/osi-validation.svg?branch=master)](https://travis-ci.com/OpenSimulationInterface/osi-validation)

OSI Validator checks the compliance of OSI messages with predefined [rules](https://opensimulationinterface.github.io/osi-documentation/osi-validation/doc/osivalidator.html#module-osivalidator.osi_rules_implementations). The full documentation on the validator and customization of the rules is available [here](https://opensimulationinterface.github.io/osi-documentation/osi-validation/README.html).

## Usage

```bash
usage: osivalidator [-h] [--data DATA] [--rules RULES] [--type {SensorView,GroundTruth,SensorData}] [--output OUTPUT] [--timesteps TIMESTEPS] [--debug] [--verbose] [--parallel] [--format {separated,None}]
                    [--blast BLAST] [--buffer BUFFER]

Validate data defined at the input

optional arguments:
  -h, --help            show this help message and exit
  --data DATA           Path to the file with OSI-serialized data.
  --rules RULES, -r RULES
                        Directory with text files containig rules.
  --type {SensorView,GroundTruth,SensorData}, -t {SensorView,GroundTruth,SensorData}
                        Name of the type used to serialize data.
  --output OUTPUT, -o OUTPUT
                        Output folder of the log files.
  --timesteps TIMESTEPS
                        Number of timesteps to analyze. If -1, all.
  --debug               Set the debug mode to ON.
  --verbose, -v         Set the verbose mode to ON.
  --parallel, -p        Set parallel mode to ON.
  --format {separated,None}, -f {separated,None}
                        Set the format type of the trace.
  --blast BLAST, -bl BLAST
                        Set the in-memory storage count of OSI messages during validation.
  --buffer BUFFER, -bu BUFFER
                        Set the buffer size to retrieve OSI messages from trace file. Set it to 0 if you do not want to use buffering at all.
```

## Installation

OSI Validator has been developed with Python 3.6 within a virtual environment on Ubuntu 18.04.

#### Local (recommended)

```bash
$ git clone https://github.com/OpenSimulationInterface/osi-validation.git
$ cd osi-validation
$ git submodule update --init
$ sudo apt-get install virtualenv
$ virtualenv -p /usr/bin/python3 venv
$ source venv/bin/activate
(venv) $ cd open-simulation-interface
(venv) $ pip install .
(venv) $ cd ..
(venv) $ pip install .
```

##### Compile (optional)

```bash
(venv) $ pip install pyinstaller
(venv) $ pyinstaller osivalidator/osi_general_validator.py --onefile
```
