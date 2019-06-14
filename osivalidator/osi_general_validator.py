"""
Main class and entry point of the OSI Validator.
"""

import argparse
import os
from collections import namedtuple
from multiprocessing import Pool, Manager
from time import time
import tracemalloc

from progress.bar import Bar
from google.protobuf.json_format import MessageToDict

from .osi_rules import OSIRules
from .osi_validator_logger import OSIValidatorLogger
from .osi_id_manager import OSIIDManager
from .osi_data_container import OSIDataContainer
from .osi_rules_checker import OSIRulesChecker


def command_line_arguments():
    """ Define and handle command line interface """

    dir_path = os.path.dirname(os.path.realpath(__file__))

    parser = argparse.ArgumentParser(
        description='Validate data defined at the input',
        prog='osivalidator')
    parser.add_argument('data',
                        help='Path to the file with OSI-serialized data.',
                        type=str)
    parser.add_argument('--rules', '-r',
                        help='Directory with text files containig rules. ',
                        default=os.path.join(dir_path, 'requirements-osi-3'),
                        type=str)
    parser.add_argument('--type', '-t',
                        help='Name of the type used to serialize data.',
                        choices=['SensorView', 'GroundTruth', 'SensorData'],
                        default='SensorView',
                        type=str,
                        required=False)
    parser.add_argument('--output', '-o',
                        help='Output folder of the log files.',
                        default='output_logs',
                        type=str,
                        required=False)
    parser.add_argument('--timesteps',
                        help='Number of timesteps to analyze. If -1, all.',
                        type=int,
                        default=-1,
                        required=False)
    parser.add_argument('--debug',
                        help='Set the debug mode to ON.',
                        action="store_true")
    parser.add_argument('--verbose',
                        help='Set the verbose mode to ON.',
                        action="store_true")

    # Handle comand line arguments
    return parser.parse_args()


MANAGER = Manager()
LOGS = MANAGER.list()
BLAST_SIZE = 500
MESSAGE_TYPE = MANAGER.Value("s", "")
TIMESTAMP_ANALYZED = MANAGER.list()
LOGGER = OSIValidatorLogger()
VALIDATION_RULES = OSIRules()
LANES_HASHES = MANAGER.list()
BAR_SUFFIX = '%(index)d/%(max)d [%(elapsed_td)s]'
BAR = Bar('', suffix=BAR_SUFFIX)


def main():
    """Main method"""

    tracemalloc.start()

    start_time = time()
    # Handling of command line arguments
    arguments = command_line_arguments()

    # Set message type
    MESSAGE_TYPE.value = arguments.type

    # Instanciate Logger
    print("Instanciate logger")
    directory = arguments.output
    if not os.path.exists(directory):
        os.makedirs(directory)

    LOGGER.init(arguments.debug, arguments.verbose, directory)

    # Read data
    LOGGER.info(None, "Read data")
    data_container = OSIDataContainer()
    data_container.from_file(arguments.data, arguments.type)

    # Collect Validation Rules
    LOGGER.info(None, "Collect validation rules")
    VALIDATION_RULES.from_yaml_directory(arguments.rules)

    # Pass all timesteps or the number specified
    if arguments.timesteps != -1:
        max_timestep = arguments.timesteps
        LOGGER.info(None, f"Pass the {max_timestep} first timesteps")
    else:
        LOGGER.info(None, "Pass all timesteps")
        max_timestep = len(data_container.data)

    # Dividing in several blast to not overload the memory
    max_timestep_blast = 0

    BAR.max = max_timestep

    while max_timestep_blast < max_timestep:
        # Clear log queue
        LOGS[:] = []

        # Recreate the pool
        pool = Pool()

        # Increment the max-timestep to analyze
        max_timestep_blast += BLAST_SIZE
        first_of_blast = (max_timestep_blast-BLAST_SIZE)
        last_of_blast = min(max_timestep_blast, max_timestep)
        # LOGGER.info(None, f"Blast to {last_of_blast}")

        # Launch computation

        pool.map(
            process_timestep,
            data_container.data[first_of_blast:last_of_blast]
        )

        # for i in range(first_of_blast, last_of_blast):
        #     process_timestep(data_container.data[i])
        # print()
        # LOGGER.info(None, "Flush the logs into database")
        LOGGER.flush(LOGS)

        # LOGGER.info(None, "Clean memory")
        close_pool(pool)

    BAR.finish()

    # Grab major OSI version

    # Elapsed time
    elapsed_time = time() - start_time
    LOGGER.info(None, f"Elapsed time: {elapsed_time}")


def close_pool(pool):
    """Cleanly close a pool to free the memory"""
    pool.close()
    pool.terminate()
    pool.join()


def process_timestep(message):
    """Process one timestep"""
    # Instanciate rules checker
    current_ground_truth_dict = MessageToDict(
        message.global_ground_truth,
        preserving_proto_field_name=True,
        use_integers_for_enums=True)

    lane_hash = hash(current_ground_truth_dict['lane_boundary'].__repr__())

    ignore_lanes = lane_hash in LANES_HASHES
    id_manager = OSIIDManager(LOGGER)
    rule_checker = OSIRulesChecker(
        VALIDATION_RULES, LOGGER, id_manager, ignore_lanes)
    timestamp = rule_checker.set_timestamp(message.timestamp)
    LOGGER.log_messages[timestamp] = []
    LOGGER.debug_messages[timestamp] = []
    LOGGER.info(None, f'Analyze message of timestamp {timestamp}', False)
    if ignore_lanes:
        LOGGER.info(timestamp, f'Ignoring lanes (Hash: {lane_hash})', False)
    else:
        LOGGER.info(timestamp, f'Checking lanes (Hash: {lane_hash})', False)

    # Check if timestamp already exists
    if timestamp in TIMESTAMP_ANALYZED:
        LOGGER.error(timestamp, f"Timestamp already exists")
    TIMESTAMP_ANALYZED.append(timestamp)

    fake_field_descriptor = namedtuple('fake_field_descriptor', ['name'])
    fake_field_descriptor.name = MESSAGE_TYPE.value

    BAR.goto(len(TIMESTAMP_ANALYZED))

    # Check common rules
    rule_checker.check_message(
        [(fake_field_descriptor, message)],
        rule_checker.rules.nested_types[MESSAGE_TYPE.value],
        id_manager=id_manager)

    LOGS.extend(LOGGER.log_messages[timestamp])

    if not ignore_lanes:
        LANES_HASHES.append(lane_hash)


if __name__ == "__main__":
    main()
