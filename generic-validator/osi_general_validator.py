#!/usr/bin/ENV python3

# Standard library Imports
import argparse
import os
from collections import namedtuple
from multiprocessing import Pool
from time import time

# Local packages imports
try:
    import osi3.osi_sensordata_pb2
    import osi3.osi_sensorview_pb2
except ModuleNotFoundError:
    print('The program encountered problems while importing OSI. Check your \
    system for required dependencies. ')

# Private imports
from osi_validation_rules import OSIValidationRules
from osi_validator_logger import OSIValidatorLogger
from osi_id_manager import OSIIDManager
from osi_data_container import OSIDataContainer
from osi_rule_checker import OSIRuleChecker

# Free Functions
def command_line_arguments():
    """ Define and handle command line interface """
    parser = argparse.ArgumentParser(
        description='Validate data defined at the input')
    parser.add_argument('--rules', '-r',
                        help='Directory with text files containig rules. ',
                        default='requirements-osi-3',
                        type=str)
    parser.add_argument('--data', '-d',
                        help='Path to the file with OSI-serialized data.',
                        type=str,
                        required=True)
    parser.add_argument('--type', '-t',
                        help='Name of the message type used to serialize data.',
                        choices=['SensorView', 'GroundTruth', 'SensorData'],
                        default='SensorView',
                        type=str,
                        required=False)
    parser.add_argument('--output', '-o',
                        help='Output folder of the log files.',
                        default='output_logs',
                        type=str,
                        required=False)
    parser.add_argument('--debug',
                        help='Set the debug mode to ON.',
                        action="store_true")
    parser.add_argument('--verbose',
                        help='Set the verbose mode to ON (display in console).',
                        action="store_true")

    # Handle comand line arguments
    return parser.parse_args()

class ValidatorEnvironment:
    """Global objects of the general validator"""
    def __init__(self):
        self.id_manager = \
        self.logger = \
        self.odc = \
        self.orc = \
        self.arguments = None

ENV = None

def main():
    """Main method"""
    global ENV

    start_time = time()
    ENV = ValidatorEnvironment()
    # Handling of command line arguments
    ENV.arguments = command_line_arguments()

    # Instanciate Logger
    print("Instanciate logger")
    directory = ENV.arguments.output
    if not os.path.exists(directory):
        os.makedirs(directory)
    ENV.logger = OSIValidatorLogger(ENV.arguments.debug, ENV.arguments.verbose,
                                    directory)

    # Read data
    ENV.logger.info("Read data")
    ENV.odc = OSIDataContainer()
    ENV.odc.from_file(ENV.arguments.data, ENV.arguments.type)

    # Instanciate ID Manager
    ENV.id_manager = OSIIDManager(ENV.logger)

    # Collect Validation Rules
    ENV.logger.info("Collect validation rules")
    ovr = OSIValidationRules()
    ovr.from_yaml_directory(ENV.arguments.rules)

    # Instanciate rule checker
    ENV.orc = OSIRuleChecker(ovr, ENV.logger, ENV.id_manager)

    # Pass all timesteps
    ENV.logger.info("Pass all timesteps")

    p = Pool(8)
    p.map(process_timestep, range(0, len(ENV.odc.data)))


    # Grab major OSI version

    # Elapsed time
    elapsed_time = time() - start_time
    ENV.logger.info(f"Elapsed time: {elapsed_time}")

def process_timestep(timestep):
    """Process one timestep"""
    ENV.id_manager.reset()
    ENV.logger.info(f"Checking timestep {timestep}")
    ENV.logger.warning_messages[timestep] = []
    ENV.logger.error_messages[timestep] = []
    ENV.logger.debug_messages[timestep] = []
    sensor_view = ENV.odc.data[timestep]
    fake_field_descriptor = namedtuple('fake_field_descriptor', ['name'])
    fake_field_descriptor.name = ENV.arguments.type

    # Check common rules
    ENV.orc.check_message(timestep, [(fake_field_descriptor, sensor_view)],
                          ENV.orc.rules.nested_types[ENV.arguments.type])

    # Resolve ID and references
    ENV.id_manager.resolve_unicity(timestep)
    ENV.id_manager.resolve_references(timestep)

    ENV.logger.flush(timestep)


if __name__ == "__main__":
    main()
