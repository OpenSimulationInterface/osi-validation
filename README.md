# OSI Validator

## Presentation

The *OSI Validator* checks the compliance of the OSI messages with the KPIs
rules.

The full documentation on usage and customization of the rules is available
[here](https://ainar.github.io/osi-validation/html/).

## Requirements

The *OSI Validator* has been developed with **Python 3.7** in an Anaconda
environment. It is the only version of Python that is supported now. *OSI
Validator* should only be used with **Python 3.7**.

- *Python 3.7*
- make (for the deployment of the documentation)

## Installation

In the root directory: ``python setup.py install``

## Deployment of the documentation

All documentation is generated under *docs* directory.

### Deployment of all the documentation

*This will erase the formerly generated documentation.* This will also deploy
the KPIs documentation at the same time.

In the folder *docs*: `make gh-pages`

### Deployment of the documentation of KPIs

In the folder KPIs: `make "KPISDOCDIR=../docs/html/KPIs"`

The newly generated KPIs are in the directory *docs/html/KPIs*.