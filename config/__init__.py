"""
Config package for user account management.

This package provides configuration settings for the user account management system.
"""

# =============================================================================
# Imports
# =============================================================================
from .settings import (
    # API settings
    API_URL, MAX_RETRIES,
    
    # Logging settings
    LOG_FILE, LOG_LEVEL, LOG_FORMAT_TYPE, LOG_FORMAT_STR,
    
    # Directory settings
    LOGS_DIR, DATA_DIR,
    
    # Validation settings
    REQUIRED_FIELDS
)

__all__ = [
    # API settings
    'API_URL', 'MAX_RETRIES',
    
    # Logging settings
    'LOG_FILE', 'LOG_LEVEL', 'LOG_FORMAT_TYPE', 'LOG_FORMAT_STR',
    
    # Directory settings
    'LOGS_DIR', 'DATA_DIR',
    
    # Validation settings
    'REQUIRED_FIELDS'
]
