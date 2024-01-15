# OSI Validator
[![CI](https://github.com/OpenSimulationInterface/osi-validation/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/OpenSimulationInterface/osi-validation/actions/workflows/ci.yml)

> **_NOTE:_**  This tool is not part of the official OSI standard. It has its own release schedule. The OSI CCB is not responsible for this software but MUST be notified about pull requests.

OSI Validator checks the compliance of OSI messages with predefined [rules](https://github.com/OpenSimulationInterface/osi-validation/tree/master/rules). The full documentation on the validator and customization of the rules is available [here](https://github.com/OpenSimulationInterface/osi-validation/tree/master/doc).

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

OSI Validator has been developed with Python 3.8 within a virtual environment on Ubuntu 20.04. See [this documentation](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) for Python virtual environments.
Check for compatibility with your system the [github actions](https://github.com/OpenSimulationInterface/osi-validation/actions) CI workflow.
Currently supported are Python 3.8, 3.9, 3.10, 3.11 and 3.12 with the latest Ubuntu version.
Check the installation prerequisites of the [Open Simulation Interface](https://github.com/OpenSimulationInterface/open-simulation-interface#installation)

### Local Linux (recommended)

```bash
$ git clone https://github.com/OpenSimulationInterface/osi-validation.git
$ cd osi-validation
$ git submodule update --init
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ python3 -m pip install --upgrade pip
(.venv) $ python3 -m pip install -r requirements_develop.txt
(.venv) $ cd open-simulation-interface && python3 -m pip install . && cd ..
(.venv) $ python3 -m pip install -r requirements.txt
(.venv) $ python3 rules2yml.py -d rules
(.venv) $ python3 -m pip install .
```

### Local Windows (Git bash)

```bash
$ git clone https://github.com/OpenSimulationInterface/osi-validation.git
$ cd osi-validation
$ git submodule update --init
$ python -m venv .venv
$ source .venv/Scripts/activate
(.venv) $ python -m pip install --upgrade pip
(.venv) $ python -m pip install -r requirements_develop.txt
(.venv) $ cd open-simulation-interface && python -m pip install . && cd ..
(.venv) $ python -m pip install -r requirements.txt
(.venv) $ python rules2yml.py -d rules
(.venv) $ python -m pip install .
```

## Example command

```bash
$ osivalidator --data data/20210818T150542Z_sv_312_50_one_moving_object.txt --rules rules/
```
