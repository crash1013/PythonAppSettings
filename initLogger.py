# initLogger

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def init_logger(filename: str, level=logging.DEBUG, silent: bool = False) -> logging.Logger:
    """
    Initializes and returns a logger with both file and console handlers.

    This function creates a logger using the provided filename to determine the logger's name and the file name for logging.
    If the filename contains an extension, the logger's name will be the filename without the extension.
    If the filename does not contain an extension, the logger's name will be the filename, and a '.log' extension will be appended to the file name.

    The logger is configured with:
    - A rotating file handler that writes logs to a file, with a maximum file size of 1MB and up to 10 backup files.
    - A console handler that outputs logs to the console (sys.stdout).
    Both handlers use the same log format.

    Parameters:
    - filename (str): The base name for the log file. If it does not contain an extension, '.log' will be appended.
    - level (int, optional): The logging level threshold. Default is logging.DEBUG.

    Returns:
    - logging.Logger: The configured logger instance.

    Raises:
    - Exception: If there is an error initializing the logger, an exception is raised and printed.

    Example:
    >>> logger = init_logger('app_log')
    >>> logger.info('This is an info message')
    """
    logname = os.path.splitext(filename)[0] if '.' in filename else filename
    filename += ".log" if '.' not in filename else ''

    logger = logging.getLogger(logname)

    # Check if the logger already has handlers to avoid duplicate logs
    if not logger.hasHandlers():
        try:
            # File handler
            log_handler = RotatingFileHandler(filename, maxBytes=1000000, backupCount=10)
            log_formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')
            log_handler.setFormatter(log_formatter)
            logger.addHandler(log_handler)

            # Stream handler (console)
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(log_formatter)
            logger.addHandler(console_handler)

            logger.setLevel(level)
            if not silent:
                logger.info(f"{logname} logger starting up")
        except Exception as e:
            print(f"Failed to initialize logger {logname}: {e}")
            raise

    return logger
