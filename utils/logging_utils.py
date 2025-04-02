import logging
import sys
import time
import json
from datetime import datetime
from config import LOG_FILE, LOG_LEVEL, LOG_FORMAT_TYPE, LOG_FORMAT_STR

class JsonFormatter(logging.Formatter):
    """
    Custom formatter for JSON logging format.
    """
    def format(self, record):
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name,
            'path': record.pathname,
            'line': record.lineno
        }
        
        # Add exception info if available
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
            
        return json.dumps(log_data)

def setup_logging(log_file: str = LOG_FILE) -> None:
    """
    Configure logging to write only error logs to a file and print all logs to console.
    Supports both text and JSON formats based on configuration.
    
    Args:
        log_file: Path to the log file where error logs will be written
    
    Returns:
        None
    """
    # Create appropriate formatter based on format type
    if LOG_FORMAT_TYPE == 'json':
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(LOG_FORMAT_STR)
    
    # Set up file handler for error logs only
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    
    # Set up console handler for all logs
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)  # Use configured log level
    root_logger.handlers = []  # Clear any existing handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)