"""
User Account Creation Script

This script reads user data from a CSV file and creates user accounts by sending
the data to an API endpoint. It validates the data, skips invalid entries,
and logs errors.
"""

import csv
import os
import sys
import time
import logging
from typing import Dict

from utils import setup_logging, validate_user_data, validate_email_address, create_user
from config import REQUIRED_FIELDS, DATA_DIR



# Configure logging
setup_logging()

def create_users(file_path: str) -> Dict[str, int]:
    """
    Reads user data from a CSV file and creates users.
    Logs errors and skips rows with missing required fields.
    
    Args:
        file_path: Path to the CSV file containing user data
        
    Returns:
        Dictionary containing summary statistics:
        - success_count: Number of successfully created users
        - error_count: Number of errors during user creation
        - skipped_count: Number of rows skipped due to validation errors
    """
    if not os.path.exists(file_path):
        error_msg = f"File not found: {file_path}"
        logging.error(error_msg)
        return {"success": 0, "errors": 1, "skipped": 0}
    
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or not all(field in reader.fieldnames for field in REQUIRED_FIELDS):
                error_msg = f"CSV file missing required headers: {', '.join(REQUIRED_FIELDS)}"
                logging.error(error_msg)
                return {"success": 0, "errors": 1, "skipped": 0}
            
            # Store rows to process to make KeyboardInterrupt handling cleaner
            rows = list(reader)
                
            try:
                for row_num, row in enumerate(rows, start=2):  # Start from 2 to account for header row
                    # Validate user data (including required fields and email format)
                    is_valid, validation_error = validate_user_data(row)
                    if not is_valid:
                        error_msg = f"Row {row_num}: Skipping user creation due to {validation_error}."
                        logging.error(error_msg)
                        skipped_count += 1
                        continue
                    
                    # Validate and normalize email address if present
                    if 'email' in row and row['email']:
                        valid_email, email_error = validate_email_address(row['email'])
                        if not valid_email:
                            error_msg = f"Row {row_num}: Skipping user creation due to invalid email format: {row['email']}."
                            logging.error(error_msg)
                            skipped_count += 1
                            continue
                        else:
                            # Update with normalized email address
                            row['email'] = valid_email
                    
                    # Create user
                    success, error_message = create_user(row)
                    if success:
                        success_count += 1
                        logging.info(f"Successfully created user: {row['email']}")
                    else:
                        error_count += 1
                        error_msg = f"Row {row_num}: Error creating user {row['email']}: {error_message}"
                        logging.error(error_msg)
            except KeyboardInterrupt:
                logging.warning(f"User creation process interrupted by user after processing {success_count + error_count + skipped_count} rows")
                # Re-raise to let the main handler deal with it
                raise
    except csv.Error as e:
        error_msg = f"CSV parsing error: {str(e)}"
        logging.error(error_msg)
        return {"success": 0, "errors": 1, "skipped": 0}
    except Exception as e:
        error_msg = f"Unexpected error processing file: {str(e)}"
        logging.error(error_msg)
    
    # Create summary dictionary
    summary = {
        "success": success_count,
        "errors": error_count,
        "skipped": skipped_count
    }
    
    return summary

def main() -> int:
    """
    Main function that runs the user creation process.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Log start of process
    logging.info("Starting user creation process")
    start_time = time.time()
    
    try:
        # Get file path from command line arguments or use default
        default_file = os.path.join(DATA_DIR, "users.csv")
        file_path = sys.argv[1] if len(sys.argv) > 1 else default_file
        
        # Create users and get summary
        summary = create_users(file_path)
        
        # Log completion
        elapsed = time.time() - start_time
        logging.info(f"Completed user creation process in {elapsed:.2f}s")
    except Exception as e:
        # Log error
        elapsed = time.time() - start_time
        logging.error(f"Error in user creation process after {elapsed:.2f}s: {str(e)}")
        return 1  # Error
    
    # Return exit code based on whether there were errors
    return 0 if summary["errors"] == 0 else 1

def handle_keyboard_interrupt():
    """
    Handle keyboard interrupt (CTRL+C) gracefully.
    Prints a message and ensures proper exit.
    """
    logging.info("Operation cancelled by user")
    return 130  # Standard exit code for SIGINT

if __name__ == "__main__":
    try:
        # Run main function and get exit code
        exit_code = main()
        
        # Get the summary from create_users for display
        # This is only done when running as a script, not during imports/tests
        file_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(DATA_DIR, "users.csv")
        summary = create_users(file_path)
        print(f"\nSummary:\n  Success: {summary['success']}\n  Errors: {summary['errors']}\n  Skipped: {summary['skipped']}")

        
        sys.exit(exit_code)
    except KeyboardInterrupt:
        sys.exit(handle_keyboard_interrupt())