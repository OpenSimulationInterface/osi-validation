#!/usr/bin/env python3

# Standard library Imports
import argparse
import sys
from collections import namedtuple
import logging

# Local packages imports
try:
    import osi3.osi_sensordata_pb2
    import osi3.osi_sensorview_pb2
except ModuleNotFoundError:
    print('The program encoutered problems while importing OSI. Check your system for required dependencies. ')

# Private imports
from osi_validation_rules import OsiValidationRules
from osi_rule_checker import OsiRuleChecker
from osi_validator_logger import OSIValidatorLogger
from osi_id_manager import OSIIDManager

# Classes
# Free Functions


def command_line_arguments():
    """ Define and handle command line interface """
    parser = argparse.ArgumentParser(
        description='Validate data defined at the input with the table of requirements/')
    parser.add_argument('--rules', '-r',
                        help='Directory with text files containig rules for validator. ',
                        type=str,
                        required=True)
    parser.add_argument('--data', '-d',
                        help='Path to the file with OSI-serialized data.',
                        type=str,
                        required=True)
    parser.add_argument('--class', '-c',
                        help='Name of the class usssed to serialize the data.',
                        choices=['SensorView', 'GroundTruth', 'SensorData'],
                        default='SensorView',
                        type=str,
                        required=False)

    # Handle comand line arguments
    return parser.parse_args()


def main():
    # Handling of command line arguments
    arguments = command_line_arguments()

    # Instanciate Logger
    print("Instanciate logger")
    logging.setLoggerClass(OSIValidatorLogger)
    logger = logging.getLogger(__name__)
    logger.__init__(__name__)
    assert isinstance(logger, OSIValidatorLogger)

    # Instanciate ID Manager
    id_manager = OSIIDManager(logger)

    # Collect Validation Rules 
    print("Collect validation rules")
    ovr = OsiValidationRules(logger, id_manager)
    ovr.from_yaml_directory(arguments.rules)

    # Read the data
    print("Read the data")
    from osi_data_container import OsiDataContainer
    odc = OsiDataContainer()
    odc.from_file(arguments.data)
    sv = odc.data[0]

    # Pass the first timestamp for check
    print("Pass the first timestamp for check")
    fake_field_descriptor = namedtuple('fake_field_descriptor',['name']) 
    fake_field_descriptor.name = "SensorView"
    ovr.check_message([(fake_field_descriptor, sv)], ovr._rules['SensorView'])


    # Resolve ID and references

    id_manager.resolve_unicity()
    id_manager.resolve_references()

    # Grab major OSI version


    # Flush the log
    logger.flush()

if __name__ == "__main__":
    main()
