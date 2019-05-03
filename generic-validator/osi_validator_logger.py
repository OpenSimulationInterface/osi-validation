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
    def __init__(self, debug=False, verbose=False, output_path="",
                 to_files = False):
        print("LOGGER INIT")
        self.warning_messages = dict()
        self.debug_messages = dict()
        self.error_messages = dict()
        self.debug_mode = debug
        self.logger = logging.getLogger(__name__)

        formatter = logging.Formatter("%(levelname)-7s -- %(message)s")

        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        _time = time.time()
        # Add handlers for files
        if to_files:
            error_file_path = os.path.join(output_path, f"error_{_time}.log")
            warning_file_path = os.path.join(output_path, f"warn_{_time}.log")

            # Log errors in a file
            handler_error = logging.FileHandler(
                error_file_path, mode="a", encoding="utf-8")

            # Log warnings in another file
            handler_warning = logging.FileHandler(
                warning_file_path, mode="a", encoding="utf-8")

            # Set formatters
            handler_error.setFormatter(formatter)
            handler_warning.setFormatter(formatter)

            # Filter
            handler_error.addFilter(ErrorFilter())
            handler_warning.addFilter(WarningFilter())

            # Set level to DEBUG
            handler_error.setLevel(logging.DEBUG)
            handler_warning.setLevel(logging.DEBUG)

            self.logger.addHandler(handler_error)
            self.logger.addHandler(handler_warning)

        if verbose:
            handler_all = logging.StreamHandler(sys.stdout)
            handler_all.setFormatter(formatter)
            handler_all.setLevel(logging.DEBUG)
            self.logger.addHandler(handler_all)
        else:
            # If verbose mode is OFF, only log INFOS
            handler_info = logging.StreamHandler(sys.stdout)
            handler_info.setFormatter(formatter)
            handler_info.addFilter(InfoFilter())
            handler_info.setLevel(logging.INFO)
            self.logger.addHandler(handler_info)

        # SQLite part
        self.conn = sqlite3.connect(
            os.path.join(output_path, f'logs_{_time}.db'))
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE logs (
            severity integer,
            timestep integer,
            message text
        )""")
        self.conn.commit()
        self.cursor.close()

    def debug(self, timestep, msg, *args, **kwargs):
        """Wrapper for python debug logger"""
        self.debug_messages[timestep].append((10, timestep, msg))
        msg = "[TS " + str(timestep) + "]" + msg
        return self.logger.debug(msg, *args, **kwargs)

    def warning(self, timestep, msg, *args, **kwargs):
        """Wrapper for python warning logger"""
        self.warning_messages[timestep].append((30, timestep, msg))
        msg = "[TS " + str(timestep) + "]" + msg
        return self.logger.warning(msg, *args, **kwargs)

    def error(self, timestep, msg, *args, **kwargs):
        """Wrapper for python error logger"""
        self.error_messages[timestep].append((40, timestep, msg))
        msg = "[TS " + str(timestep) + "]" + msg
        return self.logger.error(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """Wrapper for python info logger"""
        return self.logger.info(msg, *args, **kwargs)

    def flush(self, timestep):
        """Flush the ouput"""
        self.cursor = self.conn.cursor()

        try:
            self.cursor.executemany("INSERT INTO logs VALUES (?, ?, ?)",
                                    self.warning_messages[timestep])
            self.cursor.executemany("INSERT INTO logs VALUES (?, ?, ?)",
                                    self.error_messages[timestep])
            if self.debug_mode:
                self.cursor.executemany("INSERT INTO logs VALUES (?, ?, ?)",
                                        self.debug_messages[timestep])
        except sqlite3.DatabaseError:
            print(f"Error on timestep {timestep}")

        self.conn.commit()
        self.cursor.close()

        del self.error_messages[timestep]
        del self.warning_messages[timestep]
        del self.debug_messages[timestep]

SEVERITY = {
    Severity.ERROR: 'error',
    Severity.WARN: 'warning'
}
