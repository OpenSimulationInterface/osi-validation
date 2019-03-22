#!/usr/bin/env python3

# Standard library Imports
import argparse
import os
import sys
import copy

# Local packages imports
try:
    import osi3.osi_sensordata_pb2
    import osi3.osi_sensorview_pb2
except ModuleNotFoundError:
    print('The program encoutered problems while importing OSI. Check your system for reqired dependencies. ')

# Private imports
import data_reader


# Classes
class OsiValidationRules:
    """ This class collects validation rules """

    def __init__(self):
        self._rules = dict()

    def from_dictionary(self, dictionary):
        """ Collect validion rules found in the directory. """
        try:
            for filename in os.listdir(dictionary):
                if filename.startswith('osi_') and filename.endswith('.txt'):
                    self.form_file(dictionary, filename)

        except FileNotFoundError:
            print('Error while reading files OSI-rules. Exiting!')

    def form_file(self, dictionary, filename):
        with open(os.path.join(dictionary, filename), 'r') as file:
            for line in file.readlines():

                # Empty line
                if line.strip() == '':
                    continue

                # Comment line
                if line.strip().startswith('#'):
                    continue

                # Command line
                try:
                    self.parse_line(line)
                except:
                    print('Not a validid line in file. ')
                    print(line)

    def parse_line(self, line):
        field, verb, *parameters = line.strip().split()
        print(
            f'Field {field} should comply with rule "{verb}" and parameters {parameters}')
        self._rules.setdefault(field, []).append(
            {'verb': verb, 'params': parameters})

    def _yaml_parse_message_type(self, message_type, childs):
        for child_key, child_value in childs.items():
            # Child can be a sub message type or an attribute
            # If it is actually a sub message type, we recursively go through it
            if type(child_value) is dict:
                child_message_type = ".".join((message_type, child_key))
                self._yaml_parse_message_type(
                    child_message_type, child_value)
            # Otherwise it is an attribute, we can process its rules
            else:
                self._yaml_parse_attribute(
                    message_type, child_key, child_value)

    def _yaml_parse_attribute(self, message_type, name, rules):
        field = ".".join((message_type, name))
        for rule in rules:
            if type(rule) is dict:
                verb = next(iter(rule))
                parameters = rule[verb] if type(
                    rule[verb]) is list else [rule[verb]]
            else:
                verb, *parameters = rule.split()
            self._rules.setdefault(field, []).append(
                {'verb': verb, 'params': parameters})

    def from_yaml_directory(self, path):
        """ Collect validation rules found in the directory. """
        try:
            for filename in os.listdir(path):
                if filename.startswith('osi_') and filename.endswith(('.yml', '.yaml')):
                    self.from_yaml_file(os.path.join(path, filename))

        except FileNotFoundError:
            print('Error while reading files OSI-rules. Exiting!')

    def from_yaml_file(self, path):
        rules_file = open(path)
        parsed_rules = yaml.load(rules_file)

        for message_type in parsed_rules:
            childs = parsed_rules[message_type]
            self._yaml_parse_message_type(message_type, childs)

    def get_rules(self):
        return copy.deepcopy(self._rules)

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
    validation_rules = OsiValidationRules()
    validation_rules.from_dictionary(arguments.rules)

    # Read the data

    # Pass the first timestamp for check

    # Grab major OSI version


if __name__ == "__main__":
    main()
