"""
Main class and entry point of the OSI Validator.
"""

import argparse
from multiprocessing import Pool, Manager
from tqdm import tqdm
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "."))

# Import local files
try:
    import osi_rules
    import osi_validator_logger
    import osi_rules_checker
    import osi_trace
except Exception as e:
    print(
        "Make sure you have installed the requirements with 'pip install -r requirements.txt'!"
    )
    print(e)


def check_positive_int(value):
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def command_line_arguments():
    """Define and handle command line interface"""

    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    parser = argparse.ArgumentParser(
        description="Validate data defined at the input", prog="osivalidator"
    )
    parser.add_argument(
        "--data",
        default="",
        help="Path to the file with OSI-serialized data.",
        type=str,
    )
    parser.add_argument(
        "--rules",
        "-r",
        help="Directory with text files containig rules. ",
        default=os.path.join(dir_path, "rules"),
        type=str,
    )
    parser.add_argument(
        "--type",
        "-t",
        help="Name of the type used to serialize data.",
        choices=["SensorView", "GroundTruth", "SensorData"],
        default="SensorView",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output folder of the log files.",
        default="output_logs",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--timesteps",
        help="Number of timesteps to analyze. If -1, all.",
        type=int,
        default=-1,
        required=False,
    )
    parser.add_argument(
        "--debug", help="Set the debug mode to ON.", action="store_true"
    )
    parser.add_argument(
        "--verbose", "-v", help="Set the verbose mode to ON.", action="store_true"
    )
    parser.add_argument(
        "--parallel",
        "-p",
        help="Set parallel mode to ON.",
        default=False,
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--format",
        "-f",
        help="Set the format type of the trace.",
        choices=["separated", None],
        default=None,
        type=str,
        required=False,
    )
    parser.add_argument(
        "--blast",
        "-bl",
        help="Set the in-memory storage count of OSI messages during validation.",
        default=500,
        type=check_positive_int,
        required=False,
    )
    parser.add_argument(
        "--buffer",
        "-bu",
        help="Set the buffer size to retrieve OSI messages from trace file. Set it to 0 if you do not want to use buffering at all.",
        default=1000000,
        type=check_positive_int,
        required=False,
    )

    return parser.parse_args()


MANAGER = Manager()
LOGS = MANAGER.list()
TIMESTAMP_ANALYZED = MANAGER.list()
LOGGER = osi_validator_logger.OSIValidatorLogger()
VALIDATION_RULES = osi_rules.OSIRules()
ID_TO_TS = {}
BAR_SUFFIX = "%(index)d/%(max)d [%(elapsed_td)s]"
MESSAGE_CACHE = {}


def main():
    """Main method"""

    # Handling of command line arguments
    args = command_line_arguments()

    # Instantiate Logger
    print("Instantiate logger ...")
    directory = args.output
    if not os.path.exists(directory):
        os.makedirs(directory)

    LOGGER.init(args.debug, args.verbose, directory)

    # Read data
    print("Reading data ...")
    DATA = osi_trace.OSITrace(buffer_size=args.buffer)
    DATA.from_file(path=args.data, type_name=args.type, max_index=args.timesteps)

    if DATA.timestep_count < args.timesteps:
        args.timesteps = -1

    # Collect Validation Rules
    print("Collect validation rules ...")
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

    while max_timestep_blast < max_timestep:
        # Clear log queue
        LOGS = MANAGER.list()

        # Increment the max-timestep to analyze
        max_timestep_blast += args.blast
        first_of_blast = max_timestep_blast - args.blast
        last_of_blast = min(max_timestep_blast, max_timestep)

        # Cache messages
        DATA.cache_messages_in_index_range(first_of_blast, last_of_blast)
        MESSAGE_CACHE.update(DATA.message_cache)

        if args.parallel:
            # Launch parallel computation
            # Recreate the pool
            try:
                argument_list = [
                    (i, args.type) for i in tqdm(range(first_of_blast, last_of_blast))
                ]
                with Pool() as pool:
                    pool.starmap(process_timestep, argument_list)

            except Exception as e:
                print(str(e))

            finally:
                close_pool(pool)
                print("\nClosed pool!")
        else:
            # Launch sequential computation
            try:
                for i in tqdm(range(first_of_blast, last_of_blast)):
                    process_timestep(i, args.type)

            except Exception as e:
                print(str(e))

        MESSAGE_CACHE.clear()

    DATA.trace_file.close()
    display_results()


def close_pool(pool):
    """Cleanly close a pool to free the memory"""
    pool.close()
    pool.terminate()
    pool.join()


def process_timestep(timestep, data_type):
    """Process one timestep"""
    message = MESSAGE_CACHE[timestep]
    rule_checker = osi_rules_checker.OSIRulesChecker(LOGGER)
    timestamp = rule_checker.set_timestamp(message.value.timestamp, timestep)
    ID_TO_TS[timestep] = timestamp

    LOGGER.log_messages[timestep] = []
    LOGGER.debug_messages[timestep] = []
    LOGGER.info(None, f"Analyze message of timestamp {timestamp}", False)

    with MANAGER.Lock():
        if timestamp in TIMESTAMP_ANALYZED:
            LOGGER.error(timestep, f"Timestamp already exists")
        TIMESTAMP_ANALYZED.append(timestamp)

    # Check common rules
    getattr(rule_checker, "is_valid")(
        message, VALIDATION_RULES.get_rules().get_type(data_type)
    )

    LOGS.extend(LOGGER.log_messages[timestep])


def get_message_count(data, data_type="SensorView", from_message=0, to_message=None):
    # Wrapper function for external use in combination with process_timestep
    timesteps = None

    if from_message != 0:
        print("Currently only validation from the first frame (0) is supported!")

    if to_message is not None:
        timesteps = int(to_message)

    # Read data
    print("Reading data ...")
    DATA = osi_trace.OSITrace(buffer_size=1000000)
    DATA.from_file(path=data, type_name=data_type, max_index=timesteps)

    if DATA.timestep_count < timesteps:
        timesteps = -1

    # Collect Validation Rules
    print("Collect validation rules ...")
    try:
        VALIDATION_RULES.from_yaml_directory("osi-validation/rules/")
    except Exception as e:
        print("Error collecting validation rules:", e)

    # Pass all timesteps or the number specified
    if timesteps != -1:
        max_timestep = timesteps
        LOGGER.info(None, f"Pass the {max_timestep} first timesteps")
    else:
        LOGGER.info(None, "Pass all timesteps")
        max_timestep = DATA.timestep_count

    # Dividing in several blast to not overload the memory
    max_timestep_blast = 0

    while max_timestep_blast < max_timestep:
        # Clear log queue
        LOGS[:] = []

        # Increment the max-timestep to analyze
        max_timestep_blast += 500
        first_of_blast = max_timestep_blast - 500
        last_of_blast = min(max_timestep_blast, max_timestep)

        # Cache messages
        DATA.cache_messages_in_index_range(first_of_blast, last_of_blast)
        MESSAGE_CACHE.update(DATA.message_cache)

    DATA.trace_file.close()

    return len(MESSAGE_CACHE)


# Synthetize Logs
def display_results():
    return LOGGER.synthetize_results(LOGS)


if __name__ == "__main__":
    main()
