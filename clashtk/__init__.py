import os
import logging

from .common.log import logger
from .common import i18n

# Set default logging handler to avoid "No handler found" warnings.
logger.addHandler(logging.NullHandler())

# Set default language to avoid no language error.
i18n.change_language()


# Support HiDPI in Windows
if os.name == 'nt':
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
