"""The log module for the project."""
import logging

# Common logger in the whole library
logger = logging.getLogger('clashtk')


def enable_log_for_debug():
    """Enables logging for debug purpose."""
    logger.setLevel(logging.DEBUG)
    # TODO: Add format for the logger
    logger.addHandler(logging.StreamHandler())
