import unittest
import os
import sys

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validation import validate_user_data, validate_email_address


class TestValidation(unittest.TestCase):
    """Test cases for the validation module"""
    
    def test_valid_user_data(self):
        """Test validation with valid user data"""
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "role": "user"
        }
        is_valid, error = validate_user_data(user_data)
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
    
    def test_missing_required_field(self):
        """Test validation with missing required fields"""
        # Missing email
        user_data = {
            "name": "Test User",
            "role": "user"
        }
        is_valid, error = validate_user_data(user_data)
        self.assertFalse(is_valid)
        self.assertIn("Missing required field: email", error)
        
        # Missing multiple fields
        user_data = {}
        is_valid, error = validate_user_data(user_data)
        self.assertFalse(is_valid)
        self.assertIn("Missing required field: email", error)
        self.assertIn("Missing required field: name", error)
        self.assertIn("Missing required field: role", error)
    
    def test_invalid_email_format(self):
        """Test validation with invalid email format"""
        # Test email validation directly with validate_email_address
        email = "not-an-email"
        valid_email, error = validate_email_address(email)
        self.assertIsNone(valid_email)  # Should be None for invalid email
        self.assertIsNotNone(error)     # Should have an error message


if __name__ == "__main__":
    unittest.main()
