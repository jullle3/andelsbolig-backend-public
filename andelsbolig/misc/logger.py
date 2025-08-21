import logging
import os

from andelsbolig.config.properties import LOG_LEVEL

log_format = "%(levelname)-s - [%(name)-12s] - %(message)s"


def get_logger(module_name):
    """
    Initialize logger by calling:
        logger = get_logger(__name__)
    """
    logger = logging.getLogger(module_name)
    handler = logging.StreamHandler()
    # Configure logging format
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(LOG_LEVEL)
    return logger
