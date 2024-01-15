"""
Module which contains OSIValidatorLogger and some logging filters who wrap the
Python logging module.
"""

import logging
import time

import itertools
import textwrap
from tabulate import tabulate

from functools import wraps

import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
import osi_rules


def log(func):
    """Wrapper for logging function"""

    @wraps(func)
    def wrapper(self, timestamp, msg, *args, **kwargs):
        if timestamp not in self.log_messages:
            self.log_messages[timestamp] = []
        return func(self, timestamp, msg, *args, **kwargs)

    return wrapper


class WarningFilter(logging.Filter):
    """Filter for the logger which take INFO and WARNING messages"""

    def filter(self, record):
        return record.levelno in [20, 30]


class ErrorFilter(logging.Filter):
    """Filter for the logger which take INFO and ERROR messages"""

    def filter(self, record):
        return record.levelno in [20, 40]


class InfoFilter(logging.Filter):
    """Filter which only take INFO messages"""

    def filter(self, record):
        return record.levelno == 20


class OSIValidatorLogger:
    """Wrapper for the Python logger"""

    def __init__(self, debug=False):
        self.log_messages = dict()
        self.debug_messages = dict()
        self.debug_mode = debug
        self.logger = logging.getLogger(__name__)
        self.formatter = logging.Formatter("%(levelname)-7s -- %(message)s")
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        self._is_cli_output_set = False
        self.conn = None
        self.dbname = None

    def init_cli_output(self, verbose):
        """Initialize the CLI output"""
        if self._is_cli_output_set:
            self.logger.handlers.pop()
        if verbose:
            handler_all = logging.StreamHandler(sys.stdout)
            handler_all.setFormatter(self.formatter)
            handler_all.setLevel(logging.DEBUG)
            self.logger.addHandler(handler_all)
        else:
            # If verbose mode is OFF, only log INFOS
            handler_info = logging.StreamHandler(sys.stdout)
            handler_info.setFormatter(self.formatter)
            handler_info.addFilter(InfoFilter())
            handler_info.setLevel(logging.INFO)
            self.logger.addHandler(handler_info)
        self._is_cli_output_set = True

    def init(self, debug, verbose, output_path, files=False):
        """Initialize the OSI Validator Logger. Useful to reinitialize the object."""
        self.debug_mode = debug
        self.init_logging_storage(files, output_path)
        self.init_cli_output(verbose)

    def init_logging_storage(self, files, output_path):
        """Initialize (create or set handler) for the specified logging storage"""
        timestamp = time.time()
        self._init_logging_to_files(timestamp, output_path)

    def _init_logging_to_files(self, timestamp, output_path):
        # Add handlers for files
        error_file_path = os.path.join(output_path, f"error_{timestamp}.log")
        warning_file_path = os.path.join(output_path, f"warn_{timestamp}.log")

        # Log errors in a file
        handler_error = logging.FileHandler(error_file_path, mode="a", encoding="utf-8")

        # Log warnings in another file
        handler_warning = logging.FileHandler(
            warning_file_path, mode="a", encoding="utf-8"
        )

        # Set formatters
        handler_error.setFormatter(self.formatter)
        handler_warning.setFormatter(self.formatter)

        # Filter
        handler_error.addFilter(ErrorFilter())
        handler_warning.addFilter(WarningFilter())

        # Set level to DEBUG
        handler_error.setLevel(logging.DEBUG)
        handler_warning.setLevel(logging.DEBUG)

        self.logger.addHandler(handler_error)
        self.logger.addHandler(handler_warning)

    @log
    def debug(self, timestamp, msg, *args, **kwargs):
        """Wrapper for python debug logger"""
        if self.debug_mode:
            self.debug_messages[timestamp].append((10, timestamp, msg))
        msg = "[TS " + str(timestamp) + "]" + msg
        return self.logger.debug(msg, *args, **kwargs)

    @log
    def warning(self, timestamp, msg, *args, **kwargs):
        """Wrapper for python warning logger"""
        self.log_messages[timestamp].append((30, timestamp, msg))
        msg = "[TS " + str(timestamp) + "]" + msg
        return self.logger.warning(msg, *args, **kwargs)

    @log
    def error(self, timestamp, msg, *args, **kwargs):
        """Wrapper for python error logger"""
        self.log_messages[timestamp].append((40, timestamp, msg))
        msg = "[TS " + str(timestamp) + "]" + msg
        return self.logger.error(msg, *args, **kwargs)

    @log
    def info(self, timestamp, msg, *args, **kwargs):
        """Wrapper for python info logger"""
        if timestamp:
            self.log_messages[timestamp].append((20, timestamp, msg))
        if kwargs.get("pass_to_logger"):
            return self.logger.info(msg, *args, **kwargs)
        return 0

    def synthetize_results(self, messages):
        """Aggregate the sqlite log and output a synthetized version of the
        result"""

        def ranges(i):
            group = itertools.groupby(enumerate(i), lambda x_y: x_y[1] - x_y[0])
            for _, second in group:
                second = list(second)
                yield second[0][1], second[-1][1]

        def format_ranges(ran):
            if ran[0] == ran[1]:
                return str(ran[0])
            return f"[{ran[0]}, {ran[1]}]"

        def process_timestamps(distinct_messages):
            results = []
            range_dict = {message[2]: [] for message in distinct_messages}
            for message in distinct_messages:
                if not message[1] in range_dict[message[2]]:
                    range_dict[message[2]].append(message[1])

            for message_key, timestamps in range_dict.items():
                # Timestamps need to be sorted before the ranges can be determined
                ts_ranges = ", ".join(map(format_ranges, ranges(sorted(timestamps))))
                results.append(
                    [wrapper_ranges.fill(ts_ranges), wrapper.fill(message_key)]
                )
            return results

        wrapper_ranges = textwrap.TextWrapper(width=40)
        wrapper = textwrap.TextWrapper(width=200)
        return print_synthesis("Warnings", process_timestamps(messages))


def print_synthesis(title, ranges_messages_table):
    """Print the (range, messages) table in a nice way, precessed with title and
    the number of messages"""
    headers = ["Ranges of timestamps", "Message"]
    title_string = title + " (" + str(len(ranges_messages_table)) + ") "
    table_string = tabulate(ranges_messages_table, headers=headers)
    print(title_string)
    print(table_string)
    return title_string + "\n" + table_string


SEVERITY = {
    osi_rules.Severity.INFO: "info",
    osi_rules.Severity.ERROR: "error",
    osi_rules.Severity.WARN: "warning",
}
