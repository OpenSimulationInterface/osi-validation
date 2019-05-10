import argparse
import os
from collections import namedtuple
from multiprocessing import Pool, Manager
from time import time
import tracemalloc

from osi_validation_rules import OSIValidationRules
from osi_validator_logger import OSIValidatorLogger
from osi_id_manager import OSIIDManager
from osi_data_container import OSIDataContainer
from osi_rules_checker import OSIRulesChecker


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
    parser.add_argument('--timesteps',
                        help='Number of timesteps to analyze. If -1, all.',
                        type=int,
                        default=-1,
                        required=False)
    parser.add_argument('--debug',
                        help='Set the debug mode to ON.',
                        action="store_true")
    parser.add_argument('--verbose',
                        help='Set the verbose mode to ON (display in console).',
                        action="store_true")

    # Handle comand line arguments
    return parser.parse_args()

MANAGER = Manager()
LOGS = MANAGER.list()
BLAST_SIZE = 500
MESSAGE_TYPE = MANAGER.Value("s", "")
TIMESTAMP_ANALYZED = MANAGER.list([])
LOGGER = OSIValidatorLogger()
OVR = OSIValidationRules()

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
    LOGGER.info("Read data")
    odc = OSIDataContainer()
    odc.from_file(arguments.data, arguments.type)

    # Collect Validation Rules
    LOGGER.info("Collect validation rules")
    OVR.from_yaml_directory(arguments.rules)


    # Pass all timesteps or the number specified
    if arguments.timesteps != -1:
        max_timestep = arguments.timesteps
        LOGGER.info(f"Pass the {max_timestep} first timesteps")
    else:
        LOGGER.info("Pass all timesteps")
        max_timestep = len(odc.data)


    # Dividing in several blast to not overload the memory
    max_timestep_blast = 0

    while max_timestep_blast < max_timestep:
        # Clear log queue
        LOGS[:] = []

        # Recreate the pool
        pool = Pool()

        # Increment the max-timestep to analyze
        max_timestep_blast += BLAST_SIZE
        LOGGER.info(f"Blast to {max_timestep_blast}")
        first_of_blast = (max_timestep_blast-BLAST_SIZE)
        last_of_blast = min(max_timestep_blast, max_timestep)

        # Launch computation
        pool.map(process_timestep, odc.data[first_of_blast:last_of_blast])

        LOGGER.info("Flush the logs into database")
        LOGGER.flush(LOGS)

        LOGGER.info("Clean memory")
        close_pool(pool)

    # Grab major OSI version

    # Elapsed time
    elapsed_time = time() - start_time
    LOGGER.info(f"Elapsed time: {elapsed_time}")


def close_pool(pool):
    """Cleanly close a pool to free the memory"""
    pool.close()
    pool.terminate()
    pool.join()


def process_timestep(message):
    """Process one timestep"""
    # Instanciate ID manager
    id_manager = OSIIDManager(LOGGER)

    # Instanciate rules checker
    orc = OSIRulesChecker(OVR, LOGGER, id_manager)

    timestamp = orc.set_timestamp(message.timestamp)

    LOGGER.info(f'Analyze message of timestamp {timestamp}')
    LOGGER.log_messages[timestamp] = []
    LOGGER.debug_messages[timestamp] = []

    # Check if timestamp already exists
    if timestamp in TIMESTAMP_ANALYZED:
        LOGGER.error(timestamp, f"Timestamp already exists")
    else:
        TIMESTAMP_ANALYZED.append(timestamp)

    fake_field_descriptor = namedtuple('fake_field_descriptor', ['name'])
    fake_field_descriptor.name = MESSAGE_TYPE.value

    # Check common rules
    orc.check_message([(fake_field_descriptor, message)],
                      orc.rules.nested_types[MESSAGE_TYPE.value],
                      id_manager=id_manager)
    LOGS.extend(LOGGER.log_messages[timestamp])


if __name__ == "__main__":
    main()
