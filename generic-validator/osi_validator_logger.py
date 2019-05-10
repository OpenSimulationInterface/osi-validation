import logging
import sys
import time
import os
import sqlite3

from osi_validation_rules import Severity


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

    def __init__(self, debug=False, output_path=""):
        self.log_messages = dict()
        self.debug_messages = dict()
        self.debug_mode = debug
        self.logger = logging.getLogger(__name__)
        self.conn = None
        self.cursor = None
        self.formatter = logging.Formatter("%(levelname)-7s -- %(message)s")
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        self._is_cli_output_set = False
        self.output_path = output_path

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
        self.output_path = output_path
        self.init_logging_storage(files)
        self.init_cli_output(verbose)

    def create_database(self, timestamp):
        """Create an SQLite database and set the table for logs"""
        self.conn = sqlite3.connect(
            os.path.join(self.output_path, f'logs_{timestamp}.db'))
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE logs (
            severity integer,
            timestamp integer,
            message text
        )""")
        self.conn.commit()
        self.cursor.close()

    def init_logging_storage(self, files):
        """Initialize (create or set handler) for the specified logging storage
        """
        timestamp = time.time()
        if files:
            self._init_logging_to_files(timestamp)
        else:
            self.create_database(timestamp)

    def _init_logging_to_files(self, timestamp):
        # Add handlers for files
        error_file_path = os.path.join(self.output_path,
                                       f"error_{timestamp}.log")
        warning_file_path = os.path.join(self.output_path,
                                         f"warn_{timestamp}.log")

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

    def info(self, msg, *args, **kwargs):
        """Wrapper for python info logger"""
        return self.logger.info(msg, *args, **kwargs)

    def flush(self, log_queue=None, timestamp=None):
        """Flush the ouput to the database"""

        # Open a new cursor
        self.cursor = self.conn.cursor()

        if timestamp is not None:
            log_tuples = self.log_messages[timestamp]
        elif log_queue is not None:
            log_tuples = log_queue

        self.cursor.executemany(
            "INSERT INTO logs VALUES (?, ?, ?)", log_tuples)

        # Commit to the database and close the cursor
        self.conn.commit()
        self.cursor.close()

        if timestamp is not None:
            del self.log_messages[timestamp]
            if self.debug_mode:
                del self.debug_messages[timestamp]
        else:
            del self.log_messages
            self.log_messages = dict()


SEVERITY = {
    Severity.ERROR: 'error',
    Severity.WARN: 'warning'
}
