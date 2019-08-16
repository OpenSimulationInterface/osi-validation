"""
Main class and entry point of the OSI Validator.
"""

import argparse
import os
from multiprocessing import Pool, Manager

from progress.bar import Bar

from osivalidator.osi_rules import OSIRules
from osivalidator.osi_validator_logger import OSIValidatorLogger
from osivalidator.osi_scenario import OSIScenario
from osivalidator.osi_rules_checker import OSIRulesChecker


def command_line_arguments():
    """ Define and handle command line interface """

    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

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
BLAST_SIZE = 2000
MESSAGE_TYPE = MANAGER.Value("s", "")
TIMESTAMP_ANALYZED = MANAGER.list()
LOGGER = OSIValidatorLogger()
VALIDATION_RULES = OSIRules()
DATA = OSIScenario()
ID_TO_TS = MANAGER.dict()
BAR_SUFFIX = '%(index)d/%(max)d [%(elapsed_td)s]'
BAR = Bar('', suffix=BAR_SUFFIX)
MESSAGE_CACHE = MANAGER.dict()


def main():
    """Main method"""

    # Handling of command line arguments
    args = command_line_arguments()

    # Set message type
    MESSAGE_TYPE.value = args.type

    # Instanciate Logger
    print("Instanciate logger")
    directory = args.output
    if not os.path.exists(directory):
        os.makedirs(directory)

    LOGGER.init(args.debug, args.verbose, directory)

    # Read data
    print("Read data")
    DATA.from_file(path=args.data, type_name=args.type,
                   max_index=args.timesteps)

    # Collect Validation Rules
    print("Collect validation rules")
    # VALIDATION_RULES.from_xml_doxygen()
    VALIDATION_RULES.from_yaml_directory(args.rules)

    # Pass all timesteps or the number specified
    if args.timesteps != -1:
        max_timestep = args.timesteps
        LOGGER.info(None, f"Pass the {max_timestep} first timesteps")
    else:
        LOGGER.info(None, "Pass all timesteps")
        max_timestep = DATA.timestep_count

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

        # Cache messages
        DATA.cache_messages_in_index_range(first_of_blast, last_of_blast)
        MESSAGE_CACHE.update(DATA.message_cache)

        # Launch computation
        # TODO Change this to parallel processing
        for i in range(first_of_blast, last_of_blast):
            process_timestep(i)
        # pool.map(process_timestep, range(first_of_blast, last_of_blast))

        LOGGER.flush(LOGS)

        MESSAGE_CACHE.clear()
        close_pool(pool)

    BAR.finish()

    # Grab major OSI version

    # Synthetize
    LOGGER.synthetize_results_from_sqlite()


def close_pool(pool):
    """Cleanly close a pool to free the memory"""
    pool.close()
    pool.terminate()
    pool.join()


def process_timestep(timestep):
    """Process one timestep"""
    message = MESSAGE_CACHE[timestep]
    rule_checker = OSIRulesChecker(LOGGER)
    timestamp = rule_checker.set_timestamp(message.value.timestamp, timestep)
    ID_TO_TS[timestep] = timestamp

    LOGGER.log_messages[timestep] = []
    LOGGER.debug_messages[timestep] = []
    LOGGER.info(None, f'Analyze message of timestamp {timestamp}', False)

    # Check if timestamp already exists
    if timestamp in TIMESTAMP_ANALYZED:
        LOGGER.error(timestep, f"Timestamp already exists")
    TIMESTAMP_ANALYZED.append(timestamp)

    BAR.goto(len(TIMESTAMP_ANALYZED))

    # Check common rules
    getattr(rule_checker, 'is_valid')(
        message, VALIDATION_RULES.get_rules().get_type(MESSAGE_TYPE.value))

    LOGS.extend(LOGGER.log_messages[timestep])


if __name__ == "__main__":
    main()
