"""
Logging utility module for SmartHire AI.
Provides centralized logging across all services.
"""

import logging
import sys
from app.utils.config import LOG_LEVEL, LOG_FORMAT

# Create logger
logger = logging.getLogger("SmartHire")
logger.setLevel(LOG_LEVEL)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(LOG_LEVEL)

# Create formatter
formatter = logging.Formatter(LOG_FORMAT)
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)


def get_logger(name: str = "SmartHire"):
    """
    Get or create a logger with the given name.
    
    Args:
        name (str): Logger name
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)