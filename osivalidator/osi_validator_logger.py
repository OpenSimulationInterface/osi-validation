"""
Module which contains OSIValidatorLogger and some logging filters who wrap the
Python logging module.
"""

import logging
import sys
import time
import os
import sqlite3

import itertools
import textwrap

from functools import wraps
from tabulate import tabulate
import colorama

from .osi_rules import Severity


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


class OSIValidatorLogger():
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
        """Initialize the OSI Validator Logger. Useful to reinit the object."""
        self.debug_mode = debug
        self.init_logging_storage(files, output_path)
        self.init_cli_output(verbose)

    def create_database(self, timestamp, output_path):
        """Create an SQLite database and set the table for logs"""
        self.dbname = os.path.join(output_path, f'logs_{timestamp}.db')
        self.conn = sqlite3.connect(self.dbname)

        cursor = self.conn.cursor()

        cursor.execute("""CREATE TABLE logs (
            severity integer,
            timestamp integer,
            message text
        )""")

        self.conn.commit()
        cursor.close()

    def init_logging_storage(self, files, output_path):
        """Initialize (create or set handler) for the specified logging storage
        """
        timestamp = time.time()
        if files:
            self._init_logging_to_files(timestamp, output_path)
        else:
            self.create_database(timestamp, output_path)

    def _init_logging_to_files(self, timestamp, output_path):
        # Add handlers for files
        error_file_path = os.path.join(output_path, f"error_{timestamp}.log")
        warning_file_path = os.path.join(output_path, f"warn_{timestamp}.log")

        # Log errors in a file
        handler_error = logging.FileHandler(
            error_file_path, mode="a", encoding="utf-8")

        # Log warnings in another file
        handler_warning = logging.FileHandler(
            warning_file_path, mode="a", encoding="utf-8")

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

    def flush(self, log_queue=None, timestamp=None, from_id=None):
        """Flush the ouput to the database

        :param log_queue: list of tuple of messages that have to be flushed
        :param timestamp: if not None, only the timestamp given will be flushed
        :param from_id: if None, the timestamp will be in millisecond,
                        otherwhise it will be the id of the timestamp according
                        to the lookup table given in this parameter
        """

        # Open a new cursor
        cursor = self.conn.cursor()

        if timestamp is not None:
            log_tuples = self.log_messages[timestamp]
        elif log_queue is not None:
            log_tuples = log_queue

        if from_id:
            for tuple_id, log_tuple in enumerate(log_queue):
                log_queue[tuple_id][1] = from_id[log_tuple[1]]

        cursor.executemany("INSERT INTO logs VALUES (?, ?, ?)", log_tuples)

        # Commit to the database and close the cursor
        self.conn.commit()
        cursor.close()

        if timestamp is not None:
            del self.log_messages[timestamp]
            if self.debug_mode:
                del self.debug_messages[timestamp]
        else:
            del self.log_messages
            self.log_messages = dict()

    def synthetize_results_from_sqlite(self):
        """Aggregate the sqlite log and output a synthetized version of the
        result"""
        def ranges(i):
            group = itertools.groupby(
                enumerate(i), lambda x_y: x_y[1] - x_y[0])
            for _, second in group:
                second = list(second)
                yield second[0][1], second[-1][1]

        def format_ranges(ran):
            if ran[0] == ran[1]:
                return str(ran[0])
            return f"[{ran[0]}, {ran[1]}]"

        def process_timestamps(distinct_messages):
            results = []
            cursor = conn.cursor()
            for message in distinct_messages:
                cursor.execute(
                    """SELECT DISTINCT timestamp
                       FROM logs
                       WHERE message = ?
                       ORDER BY timestamp""",
                    message
                )

                timestamps = list(map(first_elt, cursor.fetchall()))
                ts_ranges = ", ".join(map(format_ranges, ranges(timestamps)))
                results.append([wrapper_ranges.fill(ts_ranges),
                                wrapper.fill(first_elt(message))])
            return results

        def first_elt(iterable):
            return iterable[0]

        wrapper_ranges = textwrap.TextWrapper(width=40)
        wrapper = textwrap.TextWrapper(width=200)

        conn = self.conn

        cursor_warn = conn.cursor()
        distinct_messages_w = cursor_warn.execute(
            'SELECT DISTINCT message FROM logs WHERE severity = 30')
        cursor_error = conn.cursor()
        distinct_messages_e = cursor_error.execute(
            'SELECT DISTINCT message FROM logs WHERE severity = 40')

        conn.commit()

        colorama.init()

        print()
        print_synthesis("Errors", "RED",
                        process_timestamps(distinct_messages_e))
        print()
        print_synthesis("Warnings", "YELLOW",
                        process_timestamps(distinct_messages_w))


def print_synthesis(title, color, ranges_messages_table):
    """Print the (range, messages) table in a nice way, precessed with title and
    the number of messages"""
    headers = ["Ranges of timestamps", "Message"]
    print(getattr(colorama.Fore, color) + title + " (" +
          str(len(ranges_messages_table)) + ") " + colorama.Style.RESET_ALL)
    print(tabulate(ranges_messages_table, headers=headers))


SEVERITY = {
    Severity.INFO: 'info',
    Severity.ERROR: 'error',
    Severity.WARN: 'warning'
}
