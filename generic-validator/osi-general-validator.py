#!/usr/bin/env python3

# Standard library Imports
import argparse
import sys

# Local packages imports
try:
    import osi3.osi_sensordata_pb2
    import osi3.osi_sensorview_pb2
except ModuleNotFoundError:
    print('The program encoutered problems while importing OSI. Check your system for required dependencies. ')

# Private imports
import data_reader
import osi_validation_rules

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

    # Collect Validation Rules
    validation_rules = osi_validation_rules.OsiValidationRules()
    validation_rules.from_directory(arguments.rules)

    # Read the data

    # Pass the first timestamp for check

    # Grab major OSI version


if __name__ == "__main__":
    main()
