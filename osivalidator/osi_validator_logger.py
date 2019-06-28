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
import sqlite3

from tabulate import tabulate
import colorama

from .osi_rules import Severity


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

    def debug(self, timestamp, msg, *args, **kwargs):
        """Wrapper for python debug logger"""
        if self.debug_mode:
            self.debug_messages[timestamp].append((10, timestamp, msg))
        msg = "[TS " + str(timestamp) + "]" + msg
        return self.logger.debug(msg, *args, **kwargs)

    def warning(self, timestamp, msg, *args, **kwargs):
        """Wrapper for python warning logger"""
        self.log_messages[timestamp].append((30, timestamp, msg))
        msg = "[TS " + str(timestamp) + "]" + msg
        return self.logger.warning(msg, *args, **kwargs)

    def error(self, timestamp, msg, *args, **kwargs):
        """Wrapper for python error logger"""
        self.log_messages[timestamp].append((40, timestamp, msg))
        msg = "[TS " + str(timestamp) + "]" + msg
        return self.logger.error(msg, *args, **kwargs)

    def info(self, timestamp, msg, pass_to_logger=True, *args, **kwargs):
        """Wrapper for python info logger"""
        if timestamp:
            self.log_messages[timestamp].append((20, timestamp, msg))
        if pass_to_logger:
            return self.logger.info(msg, *args, **kwargs)

    def flush(self, log_queue=None, timestamp=None, from_id=None):
        """Flush the ouput to the database"""

        # Open a new cursor
        cursor = self.conn.cursor()

        if timestamp is not None:
            log_tuples = self.log_messages[timestamp]
        elif log_queue is not None:
            log_tuples = log_queue

        if from_id:
            for tuple_id in range(len(log_queue)):
                log_queue[tuple_id][1] = from_id[log_queue[tuple_id][1]]

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
        def ranges(i):
            for a, b in itertools.groupby(enumerate(i), lambda x_y: x_y[1] - x_y[0]):
                b = list(b)
                yield b[0][1], b[-1][1]

        def format_ranges(r):
            if r[0] == r[1]:
                return str(r[0])
            else:
                return f"[{r[0]}, {r[1]}]"

        def process_timestamps(distinct_messages):
            results = []
            c2 = conn.cursor()
            for message in distinct_messages:
                c2.execute(
                    "SELECT DISTINCT timestamp FROM logs WHERE message = ? ORDER BY timestamp", message)
                timestamps = list(map(extract_from_tuple, c2.fetchall()))
                ts_ranges = ", ".join(map(format_ranges, ranges(timestamps)))
                results.append([wrapper_ranges.fill(ts_ranges),
                                wrapper.fill(extract_from_tuple(message))])
            return results

        def extract_from_tuple(t): return t[0]

        wrapper_ranges = textwrap.TextWrapper(width=40)
        wrapper = textwrap.TextWrapper(width=70)

        conn = sqlite3.connect(self.dbname)

        c = conn.cursor()
        distinct_messages_w = c.execute(
            'SELECT DISTINCT message FROM logs WHERE severity = 30')
        c3 = conn.cursor()
        distinct_messages_e = c3.execute(
            'SELECT DISTINCT message FROM logs WHERE severity = 40')

        results_w = process_timestamps(distinct_messages_w)
        results_e = process_timestamps(distinct_messages_e)
        conn.commit()
        conn.close()

        colorama.init()
        print(colorama.Fore.RED + "Errors (" + str(len(results_e)) + ") " +
              colorama.Style.RESET_ALL)
        print(tabulate(results_e, headers=["Ranges of timestamps", "Message"]))
        print()
        print(colorama.Fore.YELLOW + "Warnings (" +
              str(len(results_w)) + ") " + colorama.Style.RESET_ALL)
        print(tabulate(results_w, headers=["Ranges of timestamps", "Message"]))


SEVERITY = {
    Severity.ERROR: 'error',
    Severity.WARN: 'warning'
}
