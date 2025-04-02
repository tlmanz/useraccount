# User Account Creation System

This system automates the creation of user accounts from a CSV file. It reads user data and sends it to an API endpoint for processing.

## Features

- Reads user data from a CSV file
- Validates required fields (name, email, role)
- Validates email format
- Skips rows with missing required fields or invalid data
- Logs errors to a file (error_log.txt)
- Provides a summary of successful, failed, and skipped user creations
- Implements Python type hints for better code quality
- Follows modular design principles with a separate utils package

## Project Structure

- `main.py` - The main script for creating users
- `users.csv` - Sample CSV file with user data
- `requirements.txt` - Dependencies
- `config/` - Package containing configuration settings
  - `__init__.py` - Package initialization file
  - `settings.py` - Configuration variables and defaults
- `utils/` - Package containing utility functions
  - `__init__.py` - Package initialization file
  - `validation.py` - User data validation functions
  - `api.py` - API communication functions
  - `logging_utils.py` - Logging configuration
- `tests/` - Package containing unit tests
  - `test_api.py` - Tests for API functions
  - `test_validation.py` - Tests for validation functions
  - `test_config.py` - Tests for configuration
  - `test_logging_utils.py` - Tests for logging utilities
  - `test_main.py` - Tests for main functionality

## Setup and Usage

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the user creation script:
   ```
   python main.py [path_to_csv_file]
   ```
   If no file path is provided, it defaults to `users.csv`.

## Testing

Run the tests using Python's built-in unittest framework:

```
python -m unittest discover -s tests -p "test_*.py"
```

This will discover and run all tests in the `tests` directory that match the pattern `test_*.py`.

## CSV Format

The CSV file should have the following columns:
- `name` - User's name (required)
- `email` - User's email address (required, must be valid format)
- `role` - User's role (admin, user, moderator, etc.) (required)

## Error Handling

Errors are logged to `error_log.txt` with timestamps and detailed error messages. The script handles several types of errors:

- Missing required fields
- Invalid email format
- API connection issues
- Server-side errors

All errors are both printed to the console and logged to the error file for reference.