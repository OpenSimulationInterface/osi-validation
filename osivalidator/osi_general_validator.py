"""
Main class and entry point of the OSI Validator.
"""

import argparse
from multiprocessing import Pool, Manager
from tqdm import tqdm
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "."))

# Import local files
try:
    import osi_rules
    import osi_validator_logger
    import osi_rules_checker
    import linked_proto_field
    from format.OSITrace import OSITrace
except Exception as e:
    print(
        "Make sure you have installed the requirements with 'python3 -m pip install -r requirements.txt'!"
    )
    print(e)

# Global variables
manager_ = Manager()
logs_ = manager_.list()
timestamp_analyzed_ = manager_.list()
logger_ = osi_validator_logger.OSIValidatorLogger()
validation_rules_ = osi_rules.OSIRules()
id_to_ts_ = {}
bar_suffix_ = "%(index)d/%(max)d [%(elapsed_td)s]"
message_cache_ = {}


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
        help="Set the buffer size to retrieve OSI messages from trace file."
        "Set it to 0 if you do not want to use buffering at all.",
        default=1000000,
        type=check_positive_int,
        required=False,
    )

    return parser.parse_args()


def main():
    """Main method"""

    # Handling of command line arguments
    args = command_line_arguments()

    # Instantiate Logger
    print("Instantiate logger ...")
    directory = args.output
    if not os.path.exists(directory):
        os.makedirs(directory)

    logger_.init(args.debug, args.verbose, directory)

    # Read data
    print("Reading data ...")
    trace_data = OSITrace(buffer_size=args.buffer)
    trace_data.from_file(path=args.data, type_name=args.type, max_index=args.timesteps)

    if trace_data.timestep_count < args.timesteps:
        args.timesteps = -1

    # Collect Validation Rules
    print("Collect validation rules ...")
    validation_rules_.from_yaml_directory(args.rules)

    # Pass all timesteps or the number specified
    if args.timesteps != -1:
        max_timestep = args.timesteps
        logger_.info(None, f"Pass the {max_timestep} first timesteps")
    else:
        logger_.info(None, "Pass all timesteps")
        max_timestep = trace_data.timestep_count

    # Dividing in several blast to not overload the memory
    max_timestep_blast = 0

    while max_timestep_blast < max_timestep:
        # Clear log queue
        logs_ = manager_.list()

        # Increment the max-timestep to analyze
        max_timestep_blast += args.blast
        first_of_blast = max_timestep_blast - args.blast
        last_of_blast = min(max_timestep_blast, max_timestep)

        # Cache messages
        trace_data.cache_messages_in_index_range(first_of_blast, last_of_blast)
        message_cache_.update(trace_data.message_cache)

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

        message_cache_.clear()

    trace_data.trace_file.close()
    display_results()


def close_pool(pool):
    """Cleanly close a pool to free the memory"""
    pool.close()
    pool.terminate()
    pool.join()


def process_timestep(timestep, data_type):
    """Process one timestep"""
    message = linked_proto_field.LinkedProtoField(
        message_cache_[timestep], name=data_type
    )
    rule_checker = osi_rules_checker.OSIRulesChecker(logger_)
    timestamp = rule_checker.set_timestamp(message.value.timestamp, timestep)
    id_to_ts_[timestep] = timestamp

    logger_.log_messages[timestep] = []
    logger_.debug_messages[timestep] = []
    logger_.info(None, f"Analyze message of timestamp {timestamp}", False)

    with manager_.Lock():
        if timestamp in timestamp_analyzed_:
            logger_.error(timestep, f"Timestamp already exists")
        timestamp_analyzed_.append(timestamp)

    # Check common rules
    getattr(rule_checker, "is_valid")(
        message, validation_rules_.get_rules().get_type(data_type)
    )

    logs_.extend(logger_.log_messages[timestep])


def get_message_count(data, data_type="SensorView", from_message=0, to_message=None):
    # Wrapper function for external use in combination with process_timestep
    time_steps = None

    if from_message != 0:
        print("Currently only validation from the first frame (0) is supported!")

    if to_message is not None:
        time_steps = int(to_message)

    # Read data
    print("Reading data ...")
    trace_data = OSITrace(buffer_size=1000000)
    trace_data.from_file(path=data, type_name=data_type, max_index=time_steps)

    if trace_data.timestep_count < time_steps:
        time_steps = -1

    # Collect Validation Rules
    print("Collect validation rules ...")
    try:
        validation_rules_.from_yaml_directory("osi-validation/rules/")
    except Exception as e:
        print("Error collecting validation rules:", e)

    # Pass all time_steps or the number specified
    if time_steps != -1:
        max_timestep = time_steps
        logger_.info(None, f"Pass the {max_timestep} first time_steps")
    else:
        logger_.info(None, "Pass all time_steps")
        max_timestep = trace_data.timestep_count

    # Dividing in several blast to not overload the memory
    max_timestep_blast = 0

    while max_timestep_blast < max_timestep:
        # Clear log queue
        logs_[:] = []

        # Increment the max-timestep to analyze
        max_timestep_blast += 500
        first_of_blast = max_timestep_blast - 500
        last_of_blast = min(max_timestep_blast, max_timestep)

        # Cache messages
        trace_data.cache_messages_in_index_range(first_of_blast, last_of_blast)
        message_cache_.update(trace_data.message_cache)

    trace_data.trace_file.close()

    return len(message_cache_)


# Synthesize Logs
def display_results():
    return logger_.synthetize_results(logs_)


if __name__ == "__main__":
    main()
