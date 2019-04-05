import logging
import sys
import time
import os


class WarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in [20, 30]


class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in [20, 40]


class OSIValidatorLogger():

    def __init__(self, debug=False, output_path="", *args):
        self.warning_messages = []
        self.debug_messages = []
        self.error_messages = []

        _time = time.time()

        error_file_path = os.path.join(output_path, f"error_{_time}.log")
        warning_file_path = os.path.join(output_path, f"warning_{_time}.log")

        formatter = logging.Formatter(
            "%(levelname)-7s -- %(message)s")
        handler_error = logging.FileHandler(
            error_file_path, mode="a", encoding="utf-8")
        handler_warning = logging.FileHandler(
            warning_file_path, mode="a", encoding="utf-8")
        handler_all = logging.StreamHandler(sys.stdout)

        handler_error.setFormatter(formatter)
        handler_warning.setFormatter(formatter)
        handler_all.setFormatter(formatter)

        handler_error.addFilter(ErrorFilter())
        handler_warning.addFilter(WarningFilter())

        handler_error.setLevel(logging.DEBUG)
        handler_warning.setLevel(logging.DEBUG)
        handler_all.setLevel(logging.DEBUG)

        self.logger = logging.getLogger(__name__)

        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler_error)
        self.logger.addHandler(handler_warning)
        self.logger.addHandler(handler_all)

    def debug(self, msg, *args, **kwargs):
        self.debug_messages.append(msg)
        return self.logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.warning_messages.append(msg)
        return self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.error_messages.append(msg)
        return self.logger.error(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        return self.logger.info(msg, *args, **kwargs)

    def flush(self):
        print(f"Warnings ({len(self.warning_messages)})")
        for warning_message in self.warning_messages:
            print(warning_message)
        self.warning_messages = []
        print()

        print(f"Errors ({len(self.error_messages)})")
        for error_message in self.error_messages:
            print(error_message)

        self.error_messages = []
