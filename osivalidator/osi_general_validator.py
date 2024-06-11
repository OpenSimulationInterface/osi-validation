"""
Main class and entry point of the OSI Validator.
"""

import argparse
from tqdm import tqdm
from osi3trace.osi_trace import OSITrace
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "."))

# Import local files
try:
    import osi_rules
    import osi_validator_logger
    import osi_rules_checker
    import linked_proto_field
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
        help="Path to the file with OSI-serialized data.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--rules",
        "-r",
        help="Directory with yml files containing rules. ",
        default=os.path.join(dir_path, "rules"),
        type=str,
    )
    parser.add_argument(
        "--type",
        "-t",
        help="Name of the type used to serialize data. Default is SensorView.",
        choices=[
            "SensorView",
            "SensorViewConfiguration",
            "GroundTruth",
            "HostVehicleData",
            "SensorData",
            "TrafficUpdate",
            "TrafficCommandUpdate",
            "TrafficCommand",
            "MotionRequest",
            "StreamingUpdate",
        ],
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
        help="(Ignored) Set parallel mode to ON.",
        default=False,
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--format",
        "-f",
        help="(Ignored) Set the format type of the trace.",
        choices=[None],
        default=None,
        type=str,
        required=False,
    )
    parser.add_argument(
        "--blast",
        "-bl",
        help="Set the maximum in-memory storage count of OSI messages during validation.",
        default=500,
        type=check_positive_int,
        required=False,
    )
    parser.add_argument(
        "--buffer",
        "-bu",
        help="(Ignored) Set the buffer size to retrieve OSI messages from trace file. Set it to 0 if you do not want to use buffering at all.",
        default=0,
        type=check_positive_int,
        required=False,
    )

    return parser.parse_args()


LOGS = []
LOGGER = osi_validator_logger.OSIValidatorLogger()
VALIDATION_RULES = osi_rules.OSIRules()


def detect_message_type(path: str):
    """Automatically detect the message type from the file name.
    If it cannot be detected, the function return SensorView as default.

    Args:
        path (str): Path incl. filename of the trace file

    Returns:
        Str: Message type as string, e.g. SensorData, SensorView etc.
    """
    filename = os.path.basename(path)
    if filename.find("_sd_") != -1:
        return "SensorData"
    if filename.find("_sv_") != -1:
        return "SensorView"
    if filename.find("_svc_") != -1:
        return "SensorViewConfiguration"
    if filename.find("_gt_") != -1:
        return "GroundTruth"
    if filename.find("_tu_") != -1:
        return "TrafficUpdate"
    if filename.find("_tcu_") != -1:
        return "TrafficCommandUpdate"
    if filename.find("_tc_") != -1:
        return "TrafficCommand"
    if filename.find("_hvd_") != -1:
        return "HostVehicleData"
    if filename.find("_mr_") != -1:
        return "MotionRequest"
    if filename.find("_su_") != -1:
        return "StreamingUpdate"
    return "SensorView"


def main():
    """Main method"""

    # Handling of command line arguments
    args = command_line_arguments()

    if not args.type:
        args.type = detect_message_type(args.data)

    # Instantiate Logger
    print("Instantiate logger ...")
    directory = args.output
    if not os.path.exists(directory):
        os.makedirs(directory)

    LOGGER.init(args.debug, args.verbose, directory)

    # Read data
    print("Reading data ...")
    trace = OSITrace(path=args.data, type_name=args.type)

    # Collect Validation Rules
    print("Collect validation rules ...")
    try:
        VALIDATION_RULES.from_yaml_directory(args.rules)
    except Exception as e:
        trace.close()
        print("Error collecting validation rules:", e)
        exit(1)

    # Pass all timesteps or the number specified
    if args.timesteps != -1:
        max_timestep = args.timesteps
        LOGGER.info(None, f"Pass the {max_timestep} first timesteps")
    else:
        LOGGER.info(None, "Pass all timesteps")
        max_timestep = None

    total_length = os.path.getsize(args.data)
    current_pos = 0

    with tqdm(total=total_length, unit="B", unit_scale=True, unit_divisor=1024) as pbar:
        for index, message in enumerate(trace):
            if index % args.blast == 0:
                LOGS = []
            if max_timestep and index >= max_timestep:
                pbar.update(total_length - current_pos)
                break
            try:
                process_message(message, index, args.type)
            except Exception as e:
                print(str(e))
            new_pos = trace.file.tell()
            pbar.update(new_pos - current_pos)
            current_pos = new_pos

    trace.close()
    display_results()
    if get_num_logs() > 0:
        exit(1)


def process_message(message, timestep, data_type):
    """Process one message"""
    rule_checker = osi_rules_checker.OSIRulesChecker(LOGGER)
    timestamp = rule_checker.set_timestamp(message.timestamp, timestep)

    LOGGER.log_messages[timestep] = []
    LOGGER.debug_messages[timestep] = []
    LOGGER.info(None, f"Analyze message of timestamp {timestamp}", False)

    # Check common rules
    getattr(rule_checker, "check_children")(
        linked_proto_field.LinkedProtoField(message, name=data_type),
        VALIDATION_RULES.get_rules().get_type(data_type),
    )

    LOGS.extend(LOGGER.log_messages[timestep])


# Synthetize Logs
def display_results():
    return LOGGER.synthetize_results(LOGS)


def get_num_logs():
    return len(LOGS)


if __name__ == "__main__":
    main()
