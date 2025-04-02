import unittest
from unittest.mock import patch, mock_open
import os
import sys
from io import StringIO

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main
from utils.validation import validate_email_address

class TestMain(unittest.TestCase):
    """Test cases for the main module"""
    
    @patch('os.path.exists')
    @patch('main.create_user')
    @patch('main.validate_user_data')
    @patch('main.validate_email_address')
    @patch('builtins.open', new_callable=mock_open)
    @patch('logging.error')
    @patch('logging.info')
    def test_create_users_success(self, mock_info, mock_error, mock_file, mock_validate_email, mock_validate, mock_create, mock_exists):
        """Test create_users function with successful user creation"""
        # Setup mock file existence
        mock_exists.return_value = True
        
        # Setup mock CSV data
        csv_data = """email,name,role
        alice@example.com,Alice,admin
        bob@example.com,Bob,user"""
        mock_file.return_value.__enter__.return_value = StringIO(csv_data)
        
        # Setup mock validation and creation
        mock_validate.return_value = (True, "")
        mock_validate_email.return_value = ("normalized@example.com", None)
        mock_create.return_value = (True, "User created successfully")
        
        # Call create_users
        result = main.create_users("test.csv")
        
        # Verify results
        self.assertEqual(result["success"], 2)
        self.assertEqual(result["errors"], 0)
        self.assertEqual(result["skipped"], 0)
        
        # Verify validate_user_data and create_user were called for each user
        self.assertEqual(mock_validate.call_count, 2)
        self.assertEqual(mock_create.call_count, 2)
    
    @patch('os.path.exists')
    @patch('main.create_user')
    @patch('main.validate_user_data')
    @patch('main.validate_email_address')
    @patch('builtins.open', new_callable=mock_open)
    @patch('logging.error')
    @patch('logging.info')
    def test_create_users_validation_failure(self, mock_info, mock_error, mock_file, mock_validate_email, mock_validate, mock_create, mock_exists):
        """Test create_users function with validation failures"""
        # Setup mock file existence
        mock_exists.return_value = True
        
        # Setup mock CSV data
        csv_data = """email,name,role
        alice@example.com,Alice,admin
        invalid-email,Bob,user"""
        mock_file.return_value.__enter__.return_value = StringIO(csv_data)
        
        # Setup mock validation and creation
        mock_validate.return_value = (True, "")  # All users pass required field validation
        
        # Setup email validation to pass for first user, fail for second
        mock_validate_email.side_effect = [
            ("normalized@example.com", None),  # First user has valid email
            (None, "Invalid email format")   # Second user has invalid email
        ]
        
        mock_create.return_value = (True, "User created successfully")
        
        # Call create_users
        result = main.create_users("test.csv")
        
        # Verify results
        self.assertEqual(result["success"], 1)
        self.assertEqual(result["errors"], 0)
        self.assertEqual(result["skipped"], 1)
        
        # Verify create_user was only called for the valid user
        self.assertEqual(mock_create.call_count, 1)
    
    @patch('os.path.exists')
    @patch('main.create_user')
    @patch('main.validate_user_data')
    @patch('main.validate_email_address')
    @patch('builtins.open', new_callable=mock_open)
    @patch('logging.error')
    @patch('logging.info')
    def test_create_users_api_failure(self, mock_info, mock_error, mock_file, mock_validate_email, mock_validate, mock_create, mock_exists):
        """Test create_users function with API failures"""
        # Setup mock file existence
        mock_exists.return_value = True
        
        # Setup mock CSV data
        csv_data = """email,name,role
        alice@example.com,Alice,admin
        bob@example.com,Bob,user"""
        mock_file.return_value.__enter__.return_value = StringIO(csv_data)
        
        # Setup mock validation and creation
        mock_validate.return_value = (True, "")
        mock_validate_email.return_value = ("normalized@example.com", None)
        mock_create.side_effect = [
            (True, "User created successfully"),  # First user succeeds
            (False, "API error")  # Second user fails
        ]
        
        # Call create_users
        result = main.create_users("test.csv")
        
        # Verify results
        self.assertEqual(result["success"], 1)
        self.assertEqual(result["errors"], 1)
        self.assertEqual(result["skipped"], 0)
    
    @patch('os.path.exists')
    @patch('main.create_user')
    @patch('main.validate_user_data')
    @patch('main.validate_email_address')
    @patch('builtins.open', new_callable=mock_open)
    @patch('logging.error')
    @patch('logging.info')
    def test_create_users_missing_headers(self, mock_info, mock_error, mock_file, mock_validate_email, mock_validate, mock_create, mock_exists):
        """Test create_users function with missing headers"""
        # Setup mock file existence
        mock_exists.return_value = True
        
        # Setup mock CSV data with missing required headers
        csv_data = """email,name
        alice@example.com,Alice"""
        mock_file.return_value.__enter__.return_value = StringIO(csv_data)
        
        # Call create_users
        result = main.create_users("test.csv")
        
        # Verify results - should fail due to missing 'role' header
        self.assertEqual(result["success"], 0)
        self.assertEqual(result["errors"], 1)
        self.assertEqual(result["skipped"], 0)
        
        # Verify validate_user_data and create_user were not called
        mock_validate.assert_not_called()
        mock_create.assert_not_called()
    
    @patch('main.create_users')
    @patch('logging.info')
    def test_main_function(self, mock_info, mock_create_users):
        """Test main function"""
        # Setup mock create_users
        mock_create_users.return_value = {"success": 2, "errors": 1, "skipped": 1}
        
        # Call main
        exit_code = main.main()
        
        # Note: setup_logging is called at module level, not in main function anymore
        
        # Verify create_users was called
        mock_create_users.assert_called_once()
        
        # Verify exit code (should be non-zero due to errors)
        self.assertEqual(exit_code, 1)
    
    @patch('main.create_users')
    @patch('logging.info')
    def test_main_function_success(self, mock_info, mock_create_users):
        """Test main function with all successful operations"""
        # Setup mock create_users with no errors
        mock_create_users.return_value = {"success": 2, "errors": 0, "skipped": 0}
        
        # Call main
        exit_code = main.main()
        
        # Verify exit code (should be zero for success)
        self.assertEqual(exit_code, 0)
    
    @patch('logging.info')
    def test_handle_keyboard_interrupt(self, mock_info):
        """Test keyboard interrupt handler"""
        # Call the handler
        exit_code = main.handle_keyboard_interrupt()
        
        # Verify exit code
        self.assertEqual(exit_code, 130)  # Standard exit code for SIGINT


if __name__ == "__main__":
    unittest.main()
