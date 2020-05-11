"""
Description: This is a module that serves to customize logging.

Title: logger.py

Author: theStygianArchitect
"""
import logging
import sys
from datetime import datetime
from os import getenv
from os import makedirs
from platform import node
from typing import Text
from typing import Union

try:
    import orjson as json
except ModuleNotFoundError as module_not_found_error:
    try:
        import ujson as json  # type: ignore
    except ModuleNotFoundError as module_not_found_error:
        import json  # type: ignore

try:
    import json_log_formatter  # type: ignore
except ModuleNotFoundError as module_not_found_error:
    print(module_not_found_error)
    print('Please install all required packages')
    sys.exit(1)

LOG_LEVEL = f"{getenv('LOG_LEVEL', '')}"
if not LOG_LEVEL:
    LOG_LEVEL = logging.getLevelName(20)


def _default_json_serializer(obj):
    """Create serialization method."""
    try:
        return obj.__dict__
    except AttributeError:
        return str(obj)


class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    """Customized Logger class."""

    json_lib = json

    def json_record(self, message, extra, record):
        """Customize method to include additional information."""
        extra['message'] = message
        extra['host'] = node()
        extra['function_name'] = record.funcName
        extra['module_name'] = record.module
        if 'time' not in extra:
            extra['time'] = datetime.now().isoformat()
        return extra

    def to_json(self, record):
        """Overload method to convert bytes to string."""
        try:
            return str(self.json_lib.dumps(record), 'utf-8')
        except TypeError:
            try:
                return self.json_lib.dumps(record, default=_default_json_serializer)
            except TypeError:
                return self.json_lib.dumps(record)


def set_up_stream_logging(log_name: Text = __file__,
                          log_level: Union[str, int] = LOG_LEVEL) -> logging.Logger:
    """Customize a setup for logging.

    This function exists to setup a customized logging solution. As
    well as provide a central location for logging changes.

    Currently this setup utilizes a Stream handler (stderr)

    Args:
        log_name(Text): The name of the log file.
        log_level(str, int): The minimum level to act on.

    Returns:
        A logger instance that can receive messages to log.

    """
    formatter = CustomisedJSONFormatter()
    json_handler = logging.StreamHandler()
    json_handler.setFormatter(formatter)
    logger = logging.getLogger(name=log_name)
    if not logger.handlers:
        logger.addHandler(json_handler)
    logger.setLevel(log_level)
    return logger


def set_up_file_logging(log_name: Text = __file__, log_path: Text = '.',
                        log_level: Union[str, int] = LOG_LEVEL) -> logging.Logger:
    """Customize a setup for logging.

    This function exists to setup a customized logging solution. As
    well as provide a central location for logging changes.

    Currently this setup utilizes a Stream handler (stderr)

    Args:
        log_name(Text): The name of the log file.
        log_path(Text): Optional. The path where the log is stored.
            If absolute path isn't specified then relative path will be
            used.
        log_level(str, int): Optional. The minimum level to act on.

    Raises:
        LookupError - When log_name not present

    Returns:
        A logger instance that can receive messages to logs

    """
    makedirs(log_path, exist_ok=True)
    log_file_name = f"{log_path}/{log_name}"
    formatter = CustomisedJSONFormatter()
    json_handler = logging.FileHandler(filename=log_file_name)
    json_handler.setFormatter(formatter)
    logger = logging.getLogger(name=log_name)
    if logger.handlers:
        logger.addHandler(json_handler)
    logger.setLevel(log_level)
    return logger
