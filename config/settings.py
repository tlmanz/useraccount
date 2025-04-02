"""
Configuration settings for the user account creation system
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# ============================================================================
# Environment Variables Setup
# ============================================================================

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# ============================================================================
# Directory Configuration
# ============================================================================

# Base directories for logs and data
LOGS_DIR = os.getenv("LOGS_DIR", "logs")
DATA_DIR = os.getenv("DATA_DIR", "data")

# Validate directory existence
if not os.path.exists(LOGS_DIR):
    raise FileNotFoundError(f"Logs directory '{LOGS_DIR}' does not exist. Please create it before running the application.")

if not os.path.exists(DATA_DIR):
    raise FileNotFoundError(f"Data directory '{DATA_DIR}' does not exist. Please create it before running the application.")

# ============================================================================
# API Configuration
# ============================================================================

# API endpoint and retry settings
API_URL = os.getenv("API_URL", "http://localhost:5000/api/create_user")
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# ============================================================================
# Logging Configuration
# ============================================================================

# Log file path
LOG_FILE = os.path.join(LOGS_DIR, os.getenv("LOG_FILE", "error_log.txt"))

# Log level configuration
LOG_LEVEL_STR = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL_STR, logging.INFO)

# Log format configuration
LOG_FORMAT_TYPE = os.getenv("LOG_FORMAT", "text").lower()

# Always define LOG_FORMAT_STR, even for JSON format (will be used for text format only)
LOG_FORMAT_STR = "%(asctime)s:%(levelname)s:%(message)s" if LOG_FORMAT_TYPE != "json" else ""  # Empty string for JSON format

# ============================================================================
# Data Validation Configuration
# ============================================================================
REQUIRED_FIELDS = os.getenv("REQUIRED_FIELDS", "email,name,role").split(",")
